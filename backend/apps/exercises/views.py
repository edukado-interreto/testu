from collections import Counter

from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from .file_upload_functions import FileUploadException, handle_uploaded_file
from .models import (
    CEFR,
    Exam,
    ExamReaction,
    Exercise,
    ExerciseReaction,
    Report,
    Submission,
    Tag,
)
from .serializers import (
    CreatedBySerializer,
    ExamSerializer,
    ExerciseSerializer,
    SubmissionSerializer,
    ReportSerializer,
    TagSerializer,
)

User = get_user_model()


class ExerciseFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    created_by = filters.CharFilter(method="created_by_username")
    src_lang = filters.BaseInFilter(field_name="src_lang")
    lang_learn_lang = filters.BaseInFilter(field_name="lang_learn_lang")
    tags = filters.BaseInFilter(field_name="tags__name")
    cefr_level_min = filters.TypedChoiceFilter(
        field_name="lang_learn_cefr_level_min",
        choices=CEFR.choices,
        method="cefr",
    )
    cefr_level_max = filters.TypedChoiceFilter(
        field_name="lang_learn_cefr_level_max",
        choices=CEFR.choices,
        method="cefr",
    )

    class Meta:
        model = Exercise
        fields = [
            "name",
            "created_by",
            "src_lang",
            "lang_learn_lang",
        ]

    def created_by_username(self, queryset, name, value):
        """Lookup field `created_by` with username instead of pk."""
        return queryset.filter(created_by__username=value)

    def cefr(self, queryset, name, value):
        """
        Filter `lang_learn_cefr_level_max` against `cefr_level_min`
        and `lang_learn_cefr_level_min` against `cefr_level_max`.
        """
        minmax = name[-3:]
        field_name = name.replace(minmax, {"min": "max", "max": "min"}[minmax])
        lookup_expr = {"min": "gte", "max": "lte"}[minmax]
        return queryset.filter(**{f"{field_name}__{lookup_expr}": value})


class ExamFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    created_by = filters.CharFilter(method="created_by_username")

    class Meta:
        model = Exam
        fields = [
            "name",
            "created_by",
        ]

    def created_by_username(self, queryset, name, value):
        """Lookup field `created_by` with username instead of pk."""
        return queryset.filter(created_by__username=value)


class IsAuthenticatedOrGuest(IsAuthenticated):
    def has_permission(self, request, view):
        has_guest = bool(request.data.get("guest"))

        if view.action == "create":
            if has_guest:
                return True

        return super().has_permission(request, view)


class ExerciseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ExerciseSerializer
    filterset_class = ExerciseFilter
    lookup_field = "lid"
    ordering_fields = ["likes", "created", "modified"]
    ordering = ["-likes", "-created"]

    def get_queryset(self):
        queryset = Exercise.objects.annotate(
            likes=Sum("exercisereaction__weight", default=0)
        )
        if self.action == "retrieve":
            return queryset

        lookup = Q(searchable=True)
        if self.request.user.is_authenticated:
            lookup |= Q(searchable=False) & Q(created_by=self.request.user)
        return queryset.filter(lookup).distinct().order_by("-created")

    def get_object(self):
        # Make the long ID non case sensitive:
        self.kwargs[self.lookup_field] = self.kwargs[self.lookup_field].lower()
        return super().get_object()

    @action(methods=["post"], detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, **kwargs):
        lookup = {"user": request.user, "exercise": self.get_object()}
        reaction = ExerciseReaction.objects.filter(**lookup).first()

        if reaction:
            ExerciseReaction.objects.filter(pk=reaction.pk).delete()
            return Response({"liked": None})

        weight = ExerciseReaction.objects.get_or_create(**lookup)[0].weight
        return Response({"liked": weight})


class ExamViewSet(ModelViewSet):
    queryset = Exam.objects.annotate(likes=Sum("examreaction__weight", default=0))
    serializer_class = ExamSerializer
    filterset_class = ExamFilter
    lookup_field = "lid"

    def get_permissions(self):
        if self.action == "submissions":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["get"])
    def submissions(self, request, lid=None):
        exam = self.get_object()
        if request.user != exam.created_by:
            return Response(None, status=403)
        return Response(
            SubmissionSerializer(Submission.objects.filter(exam=exam), many=True).data
        )

    @action(methods=["post"], detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, **kwargs):
        lookup = {"user": request.user, "exam": self.get_object()}
        reaction = ExamReaction.objects.filter(**lookup).first()

        if reaction:
            ExamReaction.objects.filter(pk=reaction.pk).delete()
            return Response({"liked": None})

        weight = ExamReaction.objects.get_or_create(**lookup)[0].weight
        return Response({"liked": weight})


class SubmissionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrGuest]
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Submission.objects.none()
        return Submission.objects.filter(created_by=self.request.user)


class CreatedByViewSet(ModelViewSet):
    http_method_names = ["get", "options"]
    serializer_class = CreatedBySerializer

    def get_queryset(self):
        return (
            User.objects.annotate(count=Count("exercise"))
            .order_by("-count")
            .filter(count__gt=0)
        )


class LanguageViewSet(ViewSet):
    http_method_names = ["get", "options"]

    def list(self, request):
        uri = request._request.build_absolute_uri()
        return Response({"learn": f"{uri}learn/", "source": f"{uri}source/"})

    def _list(self, field):
        return Response(
            [
                {"code": code, "count": count}
                for code, count in Counter(
                    Exercise.objects.values_list(field, flat=True)
                ).items()
            ]
        )

    @action(detail=False)
    def learn(self, request):
        return self._list("lang_learn_lang")

    @action(detail=False)
    def source(self, request):
        return self._list("src_lang")


class TagViewSet(ModelViewSet):
    http_method_names = ["get", "options"]
    serializer_class = TagSerializer

    def get_queryset(self):
        queryset = Tag.objects.annotate(count=Count("exercise")).order_by("-count")
        if self.action == "used":
            return queryset.filter(count__gt=0)
        return queryset

    @action(detail=False)
    def used(self, request):
        return self.list(request)


class ReportViewSet(ModelViewSet):
    http_method_names = ["post", "options"]
    permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializer
    queryset = Report.objects.all()


@csrf_exempt  # TODO: ĉu eblas fari tion pli bone?
def UploadView(request):
    if request.method == "POST":
        if "file" not in request.FILES:
            return JsonResponse({"error": "Missing parameter: file"}, status=400)
        if "type" not in request.POST:
            return JsonResponse({"error": "Missing parameter: type"}, status=400)

        try:
            uploaded_file = handle_uploaded_file(
                request.FILES["file"], request.POST["type"]
            )
            return JsonResponse(
                {
                    "id": uploaded_file["file"].instance.pk,
                    "name": uploaded_file["name"],
                    "url": uploaded_file["file"].url,
                    "type": uploaded_file["file"].instance.file_type,
                }
            )

        except FileUploadException as err:
            return JsonResponse({"error": str(err)}, status=400)

    return JsonResponse({"error": "No file sent"}, status=400)

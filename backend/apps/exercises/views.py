from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from .file_upload_functions import FileUploadException, handle_uploaded_file
from .models import Exam, Exercise, Submission, CEFR
from .serializers import (
    ExamSerializer,
    ExerciseSerializer,
    SheetSerializer,
    SubmissionSerializer,
)


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


class ExerciseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ExerciseSerializer
    filterset_class = ExerciseFilter
    lookup_field = "lid"

    def get_queryset(self):
        lookup = Q(searchable=True)
        if self.request.user.is_authenticated:
            lookup |= Q(searchable=False) & Q(created_by=self.request.user)
        return Exercise.objects.filter(lookup).order_by("-created")

    def get_object(self):
        self.kwargs[self.lookup_field] = self.kwargs[self.lookup_field].lower()
        return super().get_object()


class SheetViewSet(ExerciseViewSet):  # deprecated
    lookup_field = "pk"
    serializer_class = SheetSerializer


class ExamViewSet(ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
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


class SubmissionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Submission.objects.none()
        return Submission.objects.filter(created_by=self.request.user)


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

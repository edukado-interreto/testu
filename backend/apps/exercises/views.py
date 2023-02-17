from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .file_upload_functions import FileUploadException, handle_uploaded_file
from .models import Exam, Exercise, Submission
from .serializers import (
    ExamSerializer,
    ExerciseSerializer,
    SheetSerializer,
    SubmissionSerializer,
)


class ExerciseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    lookup_field = "lid"

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
            return Response({"error": "Missing parameter: file"}, status=400)
        if "type" not in request.POST:
            return Response({"error": "Missing parameter: type"}, status=400)

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

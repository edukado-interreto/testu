from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    lookup_field = "lid"


class SubmissionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


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

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

try:
    from .models import Exercise as Sheet
except ImportError:
    from .models import Sheet
from .serializers import SheetSerializer
from .file_upload_functions import handle_uploaded_file, FileUploadException


class SheetViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer


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

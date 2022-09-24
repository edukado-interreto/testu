from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from .models import Sheet
from .serializers import SheetSerializer


class SheetViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer


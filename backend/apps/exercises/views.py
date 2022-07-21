from rest_framework.viewsets import ModelViewSet

from apps.core.permissions import IsAdminUserOrReadOnly

from .models import Sheet
from .serializers import SheetSerializer


class SheetViewSet(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer

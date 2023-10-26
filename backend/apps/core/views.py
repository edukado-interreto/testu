from django.contrib.auth import get_user_model
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class DeleteAccount(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    class Meta:
        model = User

    def get_object(self):
        return self.request.user

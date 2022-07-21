from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Sheet

User = get_user_model()


class SheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sheet
        fields = "__all__"

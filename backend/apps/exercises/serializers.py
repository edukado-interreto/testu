from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Sheet, Tag

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]

    def create(self, validated_data):
        return super().create(validated_data)


class SheetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Sheet
        fields = [
            "id",
            "created",
            "modified",
            "created_by",
            "name",
            "description",
            "data",
            "src_lang",
            "lang_learn",
            "lang_learn_cefr_level_min",
            "lang_learn_cefr_level_max",
            "age_min",
            "age_max",
            "searchable",
            "tags",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        return super().create(validated_data)

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Exercise, Tag

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]

    def create(self, validated_data):
        return super().create(validated_data)


class ExerciseSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    created_by = serializers.SlugRelatedField(read_only=True, slug_field="username")
    url = serializers.URLField(source="get_absolute_url")

    class Meta:
        model = Exercise
        fields = [
            "pk",
            "id",
            "lid",
            "created",
            "modified",
            "created_by",
            "name",
            "description",
            "data",
            "src_lang",
            "lang_learn",
            "lang_learn_lang",
            "lang_learn_cefr_level_min",
            "lang_learn_cefr_level_max",
            "age_min",
            "age_max",
            "searchable",
            "tags",
            "url",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        return super().create(validated_data)

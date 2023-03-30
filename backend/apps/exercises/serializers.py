from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Exam, Exercise, Submission, Tag

User = get_user_model()


class LidField(serializers.SlugRelatedField):
    def __init__(self, model, **kwargs):
        return super().__init__(
            slug_field="lid", queryset=model._default_manager.all(), **kwargs
        )


class ExerciseSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField("username", read_only=True)
    url = serializers.URLField(source="get_absolute_url", read_only=True)
    tags = serializers.SlugRelatedField(
        "name", many=True, required=False, queryset=Tag.objects.only("name")
    )

    class Meta:
        model = Exercise
        fields = [
            "pk",
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


class SheetSerializer(ExerciseSerializer):  # deprecated
    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        return ["id"] + [f for f in fields if f not in ("pk", "lid")]


class ExamSerializer(serializers.ModelSerializer):
    lid = serializers.CharField(read_only=True)
    exercise_lid = LidField(Exercise, source="exercise", allow_null=True)
    created_by = serializers.SlugRelatedField("username", read_only=True)
    url = serializers.URLField(source="get_absolute_url", read_only=True)

    class Meta:
        model = Exam
        fields = [
            "pk",
            "lid",
            "created",
            "modified",
            "created_by",
            "name",
            "description",
            "exercise_lid",
            "accept_submission",
            "url",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        return super().create(validated_data)


class SubmissionSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField("username", read_only=True)
    exercise = serializers.JSONField(source="data")
    exercise_lid = LidField(Exercise, source="exercise", allow_null=True)
    exam_lid = LidField(Exam, source="exam", allow_null=True)

    class Meta:
        model = Submission
        fields = [
            "pk",
            "created",
            "modified",
            "created_by",
            "guest",
            "exam_lid",
            "exercise_lid",
            "exercise",
            "score",
        ]

    def create(self, validated_data):
        if user := self.context["request"].user:
            validated_data["created_by"] = user
        return super().create(validated_data)

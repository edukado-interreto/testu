from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Exam, ExamReaction, Exercise, ExerciseReaction, Submission, Tag

User = get_user_model()


class LidField(serializers.SlugRelatedField):
    def __init__(self, model, **kwargs):
        return super().__init__(
            slug_field="lid", queryset=model._default_manager.all(), **kwargs
        )


class CreatedBySerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ["id", "username", "count"]


class TagSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = Tag
        fields = ["pk", "name", "count"]


class ExerciseSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField("username", read_only=True)
    url = serializers.URLField(source="get_absolute_url", read_only=True)
    tags = serializers.SlugRelatedField(
        "name", many=True, required=False, queryset=Tag.objects.only("name")
    )
    likes = serializers.IntegerField(read_only=True)
    liked = serializers.SerializerMethodField()

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
            "likes",
            "liked",
            "url",
        ]

    def get_fields(self):
        """Remove field `data` on list view."""
        fields = super().get_fields()
        if self._context["view"].action == "list":
            fields.pop("data")
        return fields

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        return super().create(validated_data)

    def get_liked(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return None

        reaction = ExerciseReaction.objects.filter(user=user, exercise=obj).first()
        return None if reaction is None else reaction.weight


class ExamSerializer(serializers.ModelSerializer):
    lid = serializers.CharField(read_only=True)
    exercise_lid = LidField(Exercise, source="exercise", allow_null=True)
    created_by = serializers.SlugRelatedField("username", read_only=True)
    url = serializers.URLField(source="get_absolute_url", read_only=True)
    likes = serializers.IntegerField()
    liked = serializers.SerializerMethodField()

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
            "likes",
            "liked",
            "url",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        return super().create(validated_data)

    def get_liked(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return None

        reaction = ExamReaction.objects.filter(user=user, exam=obj).first()
        return None if reaction is None else reaction.weight


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
        user = self.context["request"].user
        if user.is_authenticated:
            validated_data["created_by"] = user
        return super().create(validated_data)

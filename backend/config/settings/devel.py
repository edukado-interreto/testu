from .base import *  # noqa

SHELL_PLUS_IMPORTS = [
    "from apps.core.factories import UserFactory",
    "from apps.core.serializers import UserSerializer",
    "from apps.exercises.serializers import ExerciseSerializer, ExamSerializer",
]

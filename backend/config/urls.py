from dj_rest_auth.registration.views import VerifyEmailView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, path, reverse
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.exercises.views import (
    ExamViewSet,
    ExerciseViewSet,
    SheetViewSet,
    SubmissionViewSet,
    TagViewSet,
    UploadView,
)

router = DefaultRouter()

router.register("sheets", SheetViewSet, basename="sheet")  # deprecated
router.register("exercises", ExerciseViewSet, basename="exercise")
router.register("exams", ExamViewSet, basename="exam")
router.register("submissions", SubmissionViewSet, basename="submission")
router.register("tags", TagViewSet, basename="tag")

urlpatterns = [
    path(
        "api/auth/register/",
        include("dj_rest_auth.registration.urls"),
    ),
    path("api/auth/", include(("dj_rest_auth.urls", "rest_auth"), namespace="auth")),
    path("api/v1/", include((router.urls, "api"), namespace="api")),
    path(
        "dj-rest-auth/account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    path("api/v1/upload/", UploadView),
    path("api/", RedirectView.as_view(url="/api/v1/")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

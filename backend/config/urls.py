from apps.exercises.views import ExerciseViewSet, UploadView
from dj_rest_auth.registration.views import VerifyEmailView
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register("exercises", ExerciseViewSet)
router.register("sheets", ExerciseViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/register/", include("dj_rest_auth.registration.urls")),
    path("api/v1/", include(router.urls)),
    path(
        "dj-rest-auth/account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    path("api/v1/upload/", UploadView),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

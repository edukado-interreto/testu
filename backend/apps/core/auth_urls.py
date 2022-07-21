from django.urls import path
from django.views.generic import TemplateView

from dj_rest_auth.registration.views import (
    RegisterView,
    ResendEmailVerificationView,
    VerifyEmailView,
)
from dj_rest_auth.views import (
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
    UserDetailsView,
)


urlpatterns = [
    path("user/", UserDetailsView.as_view(), name="account"),
    path("register/", RegisterView.as_view(), name="rest_register"),
    path("verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path(
        "resend-email/", ResendEmailVerificationView.as_view(), name="rest_resend_email"
    ),
    path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
    path("password/change/", PasswordChangeView.as_view(), name="rest_password_change"),
    path("whatever/<str:key>", TemplateView.as_view(), name="account_confirm_email"),
    path("whatever/", TemplateView.as_view(), name="account_email_verification_sent"),
    path(
        "change-password/<str:id>:<str:key>",
        TemplateView.as_view(),
        name="password_reset_confirm",
    ),
]

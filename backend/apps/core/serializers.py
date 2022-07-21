from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.shortcuts import get_object_or_404
from rest_framework.fields import CharField, EmailField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.validators import ValidationError

from .models import OneTimeCode
from .utils import get_url
from .validators import PASSWORD_VALIDATORS, six_digits

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "data", "date_joined"]


class RegisterSerializer(Serializer):
    email = EmailField(required=True)
    password = CharField(write_only=True, style={"input_type": "password"})

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    "A user is already registered with this e-mail address.",
                )
        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def get_cleaned_data(self):
        return {
            "password": self.validated_data.get("password", ""),
            "email": self.validated_data.get("email", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        user.email = self.validated_data["email"]
        self.cleaned_data = self.get_cleaned_data()
        if "password" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data["password"], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        user.save()
        setup_user_email(request, user, [])
        return user

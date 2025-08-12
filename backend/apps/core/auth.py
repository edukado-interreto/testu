from urllib.parse import urljoin

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.sites.models import Site
from django.urls import reverse

from allauth.account.adapter import DefaultAccountAdapter

UserModel = get_user_model()


class CustomAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        domain = Site.objects.get(name="frontend").domain
        url = reverse("account_confirm_email", args=[emailconfirmation.key])
        return urljoin(domain, url)


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            if kwargs.get("email"):
                username = kwargs["email"]
            else:
                return
        try:
            user = UserModel.objects.get(email__iexact=username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        except UserModel.MultipleObjectsReturned:
            return
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

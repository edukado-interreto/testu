from django import forms
from django.contrib.auth.forms import \
  UserCreationForm as DjangoUserCreationForm
from django.utils.translation import gettext as _


class UserCreationForm(DjangoUserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    class Meta:
        fields = ["username", "email"]

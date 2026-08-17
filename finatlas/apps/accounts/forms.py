# accounts/forms.py
from django.forms import forms

from finatlas.accounts.models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
        )

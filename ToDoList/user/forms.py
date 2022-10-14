from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Gender


class UserModifiedCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        model._meta.get_field("email")._unique = True
        fields = ["username", "email", "password1", "password2"]


class ProfileCreationForm(forms.ModelForm):
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), empty_label=None)

    class Meta:
        model = Profile
        fields = ["name", "gender"]


class UserModifiedUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["email"]


class ProfileUpdateForm(forms.ModelForm):
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), empty_label=None)

    class Meta:
        model = Profile
        fields = ["name", "gender", "profile_pic"]
        widgets = {"profile_pic": forms.FileInput()}

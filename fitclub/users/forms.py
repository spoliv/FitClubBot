from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ClubClient


class ClubClientCreationForm(UserCreationForm):

    class Meta:
        model = ClubClient
        fields = ('username', 'email')


class ClubClientChangeForm(UserChangeForm):

    class Meta:
        model = ClubClient
        fields = UserChangeForm.Meta.fields

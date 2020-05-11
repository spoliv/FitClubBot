from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import ClubClientCreationForm, ClubClientChangeForm
from .models import ClubClient


class ClubClientAdmin(UserAdmin):
    add_form = ClubClientCreationForm
    form = ClubClientChangeForm
    model = ClubClient
    list_display = ['email', 'username', 'name']


admin.site.register(ClubClient, ClubClientAdmin)


from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.ClubClientListView.as_view()),
]
from django.urls import include, path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.ClubClientListView.as_view()),
    #path('', views.CommandReceiveView.as_view()),
    #url(r'^(?P<bot_token>.+)/$', views.CommandReceiveView.as_view()),
    #url(r'^(?P<bot_token>.+)/$', views.ClubClientListView.as_view()),
]
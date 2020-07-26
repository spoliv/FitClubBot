from django.urls import include, path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('servicecategories/', views.ServiceCategoryListView.as_view()),
    path('service/<int:pk>/', views.ServiceView.as_view()),
    path('create/category/', views.ServiceCategoryCreateView.as_view()),
    path('create/service/', views.ServiceCreateView.as_view()),
    path('category/<int:pk>/', views.ServiceListView.as_view()),
]

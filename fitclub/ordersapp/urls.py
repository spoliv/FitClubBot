from django.urls import include, path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('create/date/', views.DateCreateView.as_view()),
    path('create/period/', views.PeriodCreateView.as_view()),
    path('create/order/', views.OrderCreateView.as_view()),
    path('order/<int:pk_d>/<int:pk_t>/<int:pk_s>/', views.OrderView.as_view()),
    path('dates/', views.DateListView.as_view()),
    path('date/<int:pk>/', views.DateView.as_view()),
    path('periods/', views.PeriodListView.as_view()),
    path('period/<int:pk>/', views.PeriodView.as_view()),
    path('create/card/', views.ClientCardCreateView.as_view()),
    path('create/card_item/', views.CardItemCreateView.as_view()),
    path('all/<int:pk_u>/<int:pk_c>/', views.ClientCardListView.as_view()),
    path('card_items/all/', views.CardItemListView.as_view()),
    path('create/basket/', views.BasketCreateView.as_view()),
    path('basket/<int:pk>/', views.BasketListView.as_view()),
    path('basket/<int:pk>/all/', views.BasketOnlyIdView.as_view()),

    #path('basket/last/<int:pk>/', views.BasketLastListView.as_view()),
]
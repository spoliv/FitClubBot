import os
from rest_framework import generics
from django.core.mail import EmailMessage
#from django.core import mail
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from mainfitclub.settings import config
from . import models
from . import serializers
from users.permissions import IsCardOwnerOrReadOnly


# class ServiceCategoryListView(generics.ListAPIView):
#     queryset = models.ServiceCategory.objects.all()
#     serializer_class = serializers.ServiceCategorySerializer
#
#
class OrderView(generics.ListAPIView):
    def get_queryset(self):
        queryset = super(OrderView, self).get_queryset()
        queryset = queryset.filter(date=self.kwargs['pk_d'],
                                   time_period=self.kwargs['pk_t'],
                                   service_id=self.kwargs['pk_s'])
        return queryset
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer


class DateListView(generics.ListAPIView):
    queryset = models.CalendarDate.objects.all()
    serializer_class = serializers.DateSerializer


class DateView(generics.ListAPIView):
    def get_queryset(self):
        queryset = super(DateView, self).get_queryset()
        queryset = queryset.filter(id=self.kwargs['pk'])
        return queryset
    queryset = models.CalendarDate.objects.all()
    serializer_class = serializers.DateSerializer


class PeriodListView(generics.ListAPIView):
    queryset = models.TimePeriod.objects.all()
    serializer_class = serializers.PeriodSerializer


class PeriodView(generics.ListAPIView):
    def get_queryset(self):
        queryset = super(PeriodView, self).get_queryset()
        queryset = queryset.filter(id=self.kwargs['pk'])
        return queryset
    queryset = models.TimePeriod.objects.all()
    serializer_class = serializers.PeriodSerializer


class DateCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.DateSerializer


class PeriodCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.PeriodSerializer


class OrderCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.OrderSerializer


class BasketCreateView(generics.ListCreateAPIView):

    queryset = models.Basket.objects.all()
    serializer_class = serializers.BasketCreateSerializer
    permission_classes = [IsAuthenticated, ]


class BasketOnlyIdView(generics.ListAPIView):
    def get_queryset(self):
        queryset = super(BasketOnlyIdView, self).get_queryset()
        # queryset = queryset.filter(user=self.kwargs['pk'])
        queryset = queryset.filter(user=self.request.user.id)
        return queryset
    queryset = models.Basket.objects.all()
    serializer_class = serializers.BasketOnlyIdSerializer
    permission_classes = [IsCardOwnerOrReadOnly, IsAuthenticated, ]


class BasketListView(generics.ListAPIView):
    def get_queryset(self):
        queryset = super(BasketListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user.id)
        return queryset
    queryset = models.Basket.objects.all()
    serializer_class = serializers.BasketListSerializer
    permission_classes = [IsCardOwnerOrReadOnly, IsAuthenticated, ]


# class BasketLastListView(generics.ListAPIView):
#     def get_queryset(self):
#         queryset = super(BasketLastListView, self).get_queryset()
#         queryset = queryset.filter(user=self.kwargs['pk']).first()
#         print(queryset)
#         return queryset
#     queryset = models.Basket.objects.all()
#     serializer_class = serializers.BasketListSerializer


class ClientCardCreateView(generics.ListCreateAPIView):
    queryset = models.ClientCard.objects.all()
    serializer_class = serializers.ClientCardCreateSerializer
    permission_classes = [IsAuthenticated, ]


class CardItemCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.CardItemCreateSerializer
    permission_classes = [IsAuthenticated, ]


class ClientCardListView(generics.ListAPIView):
    def get_queryset(self):
        queryset = super(ClientCardListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user.id, card_number=self.kwargs['pk_c'])
        return queryset
    queryset = models.ClientCard.objects.all()
    serializer_class = serializers.ClientCardListSerializer
    permission_classes = [IsCardOwnerOrReadOnly, ]


class ClientCardsListView(generics.ListAPIView):
    def get_queryset(self):
        queryset = super(ClientCardsListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user.id)
        return queryset
    queryset = models.ClientCard.objects.all()
    serializer_class = serializers.ClientCardsListSerializer
    permission_classes = [IsCardOwnerOrReadOnly, ]


class CardItemListView(generics.ListAPIView):
    def get_queryset(self):
        queryset = super(CardItemListView, self).get_queryset()
        queryset = queryset.select_related()
        return queryset
    queryset = models.CardItem.objects.all()
    serializer_class = serializers.CardItemDetailsSerializer


class CardActivateView(generics.UpdateAPIView):
    queryset = models.ClientCard.objects.all()
    serializer_class = serializers.ClientCardActivateSerializer
    permission_classes = [IsCardOwnerOrReadOnly, ]
    lookup_field = 'card_number'
    lookup_url_kwarg = 'pk_card'





#отправка почты


def send_email_with_attach(request, emailto):
    content = "Расписание тренировок"
    email = EmailMessage("Hello, качок", content, "o.spresov@gmail.com", [emailto])
    filename = 'myfitbot/schedule_club.pdf'
    fd = open(filename, 'rb')
    email.attach(filename, fd.read(), 'text/plain')

    res = email.send()
    return HttpResponse('%s' % res)



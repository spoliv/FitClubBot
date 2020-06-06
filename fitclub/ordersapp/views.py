from rest_framework import generics
from . import models
from . import serializers


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
    serializer_class = serializers.BasketCreateSerializer


class BasketOnlyIdView(generics.ListAPIView):
    def get_queryset(self):
        queryset = super(BasketOnlyIdView, self).get_queryset()
        queryset = queryset.filter(user=self.kwargs['pk'])
        return queryset
    queryset = models.Basket.objects.all()
    serializer_class = serializers.BasketOnlyIdSerializer


class BasketListView(generics.ListAPIView):
    def get_queryset(self):
        queryset = super(BasketListView, self).get_queryset()
        queryset = queryset.filter(user=self.kwargs['pk'])
        return queryset
    queryset = models.Basket.objects.all()
    serializer_class = serializers.BasketListSerializer


# class BasketLastListView(generics.ListAPIView):
#     def get_queryset(self):
#         queryset = super(BasketLastListView, self).get_queryset()
#         queryset = queryset.filter(user=self.kwargs['pk']).first()
#         print(queryset)
#         return queryset
#     queryset = models.Basket.objects.all()
#     serializer_class = serializers.BasketListSerializer


class ClientCardCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.ClientCardCreateSerializer


class CardItemCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.CardItemCreateSerializer


class ClientCardListView(generics.ListAPIView):
    def get_queryset(self):
        queryset = super(ClientCardListView, self).get_queryset()
        queryset = queryset.filter(user=self.kwargs['pk_u'],
                                   card_number=self.kwargs['pk_c'])
        return queryset
    queryset = models.ClientCard.objects.all()
    serializer_class = serializers.ClientCardListSerializer


class CardItemListView(generics.ListAPIView):
    def get_queryset(self):
        queryset = super(CardItemListView, self).get_queryset()
        queryset = queryset.select_related()
        return queryset
    queryset = models.CardItem.objects.all()
    serializer_class = serializers.CardItemDetailsSerializer

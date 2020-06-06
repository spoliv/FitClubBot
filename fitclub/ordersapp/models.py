from django.db import models
from mainfitclub import settings
from services.models import Service


class CalendarDate(models.Model):

    class Meta:
        verbose_name = 'Календарная дата'

    date = models.CharField(max_length=50)


class TimePeriod(models.Model):

    class Meta:
        verbose_name = 'Период времени'

    period = models.CharField(max_length=50)


class Order(models.Model):
    date = models.ForeignKey(CalendarDate, on_delete=models.CASCADE)
    time_period = models.ForeignKey(TimePeriod, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='доступное количество', default=0)
    is_active = models.BooleanField(verbose_name='активен', default=True)


# class ClientCard(models.Model):
#     set_services = models.ManyToManyField(Order, blank=True)
#     #set_services = models.ForeignKey('Order')
#
#
#     @property
#     def total_price(self):
#         qs = self.set_services.through.objects.all().aggregate(total_price=models.Sum('service__price'))
#         return qs['total_price']


class ClientCard(models.Model):
    card_number = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='card')

    @property
    def client_card_cost(self):
        return sum([
            el.service_id.price
            for el in self.card_items.select_related('service_id').all()
        ])


class CardItem(models.Model):
    client_card = models.ForeignKey(ClientCard, related_name="card_items", on_delete=models.CASCADE)
    date = models.ForeignKey(CalendarDate, on_delete=models.CASCADE)
    time_period = models.ForeignKey(TimePeriod, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    date = models.ForeignKey(CalendarDate, on_delete=models.CASCADE)
    time_period = models.ForeignKey(TimePeriod, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)


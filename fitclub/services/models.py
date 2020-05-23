from django.db import models


class ServiceCategory(models.Model):

    class Meta:
        verbose_name = 'Категория услуги'
        verbose_name_plural = 'Категории услуги'

    name = models.CharField(max_length=50)


class Service(models.Model):

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.DecimalField(verbose_name='цена услуги', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='доступное количество', default=0)
    is_active = models.BooleanField(verbose_name='активен', default=True)

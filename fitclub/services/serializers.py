from rest_framework import serializers
from . import models


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceCategory
        fields = ('id', 'name', )


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ('id', 'category', 'name', 'price', 'quantity',)

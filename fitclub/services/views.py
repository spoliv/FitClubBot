from rest_framework import generics
from . import models
from . import serializers


class ServiceCategoryListView(generics.ListAPIView):
    queryset = models.ServiceCategory.objects.all()
    serializer_class = serializers.ServiceCategorySerializer


class ServiceListView(generics.ListAPIView):
    def get_queryset(self):
        queryset = super(ServiceListView, self).get_queryset()
        queryset = queryset.filter(category=self.kwargs['pk'])
        return queryset
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer


class ServiceCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.ServiceSerializer


class ServiceCategoryCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.ServiceCategorySerializer

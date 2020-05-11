from rest_framework import generics

from . import models
from . import serializers


class ClubClientListView(generics.ListAPIView):
    queryset = models.ClubClient.objects.all()
    serializer_class = serializers.ClubClientSerializer

from rest_framework import serializers
from . import models


class ClubClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClubClient
        fields = ('email', 'username', )

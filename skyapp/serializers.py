from rest_framework import serializers

from skyapp.models import Airports


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airports
        fields = ('iata', 'name_en', 'parent_name_en')
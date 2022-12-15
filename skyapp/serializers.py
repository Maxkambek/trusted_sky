from rest_framework import serializers

from skyapp.models import Airport


class AirportSerializers(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'name', 'iata_code', 'continent', 'municipality']

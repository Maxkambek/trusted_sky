from django.db import models


class Airport(models.Model):
    iata_code = models.CharField(max_length=5, null=True)
    name = models.CharField(max_length=100, null=True)
    continent = models.CharField(max_length=10, null=True)
    municipality = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=221, null=True)
    city_code = models.CharField(max_length=4, null=True)

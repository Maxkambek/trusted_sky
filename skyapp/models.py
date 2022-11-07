from django.db import models


class Airports(models.Model):
    iata = models.CharField(max_length=5)
    name_ru = models.CharField(max_length=60)
    name_en = models.CharField(max_length=60)
    parent_name_en = models.CharField(max_length=75)

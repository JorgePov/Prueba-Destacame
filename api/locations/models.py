from django.db import models
from travels.models import Travel


class Traveler(models.Model):
    id_card = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Location(models.Model):
    traveler = models.ForeignKey(Traveler, on_delete=models.SET_NULL, null=True)
    travel = models.ForeignKey(Travel, on_delete=models.SET_NULL, null=True)
    location_number = models.IntegerField()
    travel_date = models.DateTimeField()
    boarding_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
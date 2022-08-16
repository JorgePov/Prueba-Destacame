from django.db import models
from users.models import User

class Bus(models.Model):
    bus_plate = models.CharField(max_length=10, primary_key=True)
    capacity = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Journey(models.Model):
    destination = models.CharField(max_length=20)
    origin = models.CharField(max_length=20)
    price = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Schedule(models.Model):
    departure_time = models.TimeField()
    cases_closing = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Travel(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True)
    journey = models.ForeignKey(Journey, on_delete=models.SET_NULL, null=True)
    scheduled = models.ForeignKey(Schedule, on_delete=models.SET, null=True)
    driver = models.ForeignKey(User, on_delete=models.SET)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)



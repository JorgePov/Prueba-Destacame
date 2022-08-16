from django.contrib import admin
from locations.models import Location, Traveler

@admin.register(Location)
class TravelAdmin(admin.ModelAdmin):
    list_display = ['id', 'traveler', 'travel', 'location_number', 'travel_date', 'boarding_time']

admin.site.register(Traveler)
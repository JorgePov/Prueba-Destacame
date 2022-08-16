from django.contrib import admin
from travels.models import Travel, Schedule, Journey, Bus


@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    list_display = ['id', 'bus', 'journey', 'scheduled', 'driver', 'is_active']



admin.site.register(Schedule)
admin.site.register(Journey)
admin.site.register(Bus)
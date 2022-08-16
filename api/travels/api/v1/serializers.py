from rest_framework import serializers
from travels.models import Bus, Journey, Schedule, Travel
from users.api.v1.serializers import UserSerializer

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ('bus_plate', 'capacity', 'is_active')

class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = ('id', 'destination', 'origin', 'price', 'is_active')

    def create(self, validated_data):
        try:
            destination = validated_data.get('destination')
            origin = validated_data.get('origin')
            journey = Journey.objects.get(destination=destination,origin=origin)
            if journey:
                raise serializers.ValidationError({
                            'res': f"Este trayecto [%s - %s] ya existe, se encuentra asignado al siguiente id: %s" % (destination, origin, journey.id)
                        })
        except Journey.DoesNotExist:
            return super().create(validated_data=validated_data)

class JourneyOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = ('id', 'price', 'is_active')

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'departure_time', 'cases_closing')

class TravelSerializer(serializers.ModelSerializer):
    bus =  BusSerializer()
    journey =  JourneySerializer()
    scheduled =  ScheduleSerializer()
    driver = UserSerializer()
    class Meta:
        model = Travel
        fields = ['id', 'bus', 'journey', 'scheduled', 'driver', 'is_active']

class TravelOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Travel
        fields = ['id', 'bus', 'journey', 'scheduled', 'driver', 'is_active']

    def check_schedule_availability(self, validated_data, instance=None):
        scheduled = validated_data.get('scheduled',instance)
        journey = validated_data.get('journey',None)
        if journey:
            travel_journey = Travel.objects.filter(journey__pk=journey.id, scheduled__pk=scheduled.id)
            if travel_journey:
                raise serializers.ValidationError({"res": "Ya existe un viaje para este destino en este horario"})
        bus = validated_data.get('bus',None)
        if bus:
            travel_bus = Travel.objects.filter(bus__pk=bus.bus_plate, scheduled__pk=scheduled.id)
            if travel_bus:
                raise serializers.ValidationError({"res": "El Bus ya se encuentra ocupado en ese horario"})
        
        driver = validated_data.get('driver',None)
        if driver:
            travel_driver = Travel.objects.filter(driver__pk=driver.id, scheduled__pk=scheduled.id)
            if travel_driver:
                raise serializers.ValidationError({"res": "El conductor ya se encuentra ocupado en ese horario"})

    def create(self, validated_data):
        self.check_schedule_availability(validated_data)
        return super().create(validated_data=validated_data)

    def update(self, instance, validated_data):
        self.check_schedule_availability(validated_data, instance)
        return super().update(instance=instance, validated_data=validated_data)


class TravelNoAuthSerializer(serializers.ModelSerializer):
    journey =  JourneySerializer()
    class Meta:
        model = Travel
        fields = ['id', 'journey']
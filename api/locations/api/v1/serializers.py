from rest_framework import serializers
from locations.models import Traveler, Location
from travels.models import Bus, Travel
from travels.api.v1.serializers import TravelSerializer, TravelNoAuthSerializer

class TravelerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traveler
        fields = ('id_card', 'first_name', 'last_name', 'age')

class LocationSerializer(serializers.ModelSerializer):
    traveler = TravelerSerializer()
    travel = TravelSerializer()
    class Meta:
        model = Location
        fields = ['traveler', 'travel', 'location_number', 'travel_date', 'boarding_time']


class LocationOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id','traveler', 'travel', 'location_number', 'travel_date', 'boarding_time']


    def create(self, validated_data):
        travel = validated_data.get('travel')
        if validated_data.get('location_number') > travel.bus.capacity:
            raise serializers.ValidationError(
                {"res": f"El puesto no existe, el bus tiene %s puestos" % (travel.bus.capacity)}
            )

        return super().create(validated_data=validated_data)


class LocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id','location_number']

class LocationNoAuthSerializer(serializers.ModelSerializer):
    traveler = TravelerSerializer()
    travel = TravelNoAuthSerializer()
    class Meta:
        model = Location
        fields = ['traveler', 'travel', 'location_number', 'travel_date', 'boarding_time']
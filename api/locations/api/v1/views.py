import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TravelerSerializer, LocationSerializer, LocationOperationSerializer, LocationUpdateSerializer, \
    LocationNoAuthSerializer
from .permissions import IsSellerLocations
from locations.models import Traveler, Location


class TravelerApiView(APIView):
    permission_classes = [IsSellerLocations]

    def post(self, request):
        serializer = TravelerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TravelerDetailApiView(APIView):
    permission_classes = [IsSellerLocations]
    
    def get(self, request, id_card):
        try:
            serializer = TravelerSerializer(Traveler.objects.get(id_card=id_card))
            return Response(serializer.data)
        except Traveler.DoesNotExist:
            return Response({'msg': "id not exist"},status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id_card):
        try:
            traveler = Traveler.objects.get(id_card=id_card)
            serializer = TravelerSerializer(traveler, request.data, partial = True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Traveler.DoesNotExist:
            return Response({'msg': "id not exist"},status=status.HTTP_404_NOT_FOUND)


class LocationApiView(APIView):
    permission_classes = [IsSellerLocations]


    def get(self, request):
        serializer = LocationSerializer(Location.objects.all(), many=True)
        return Response(serializer.data)


    def post(self, request):

        location = Location.objects.filter(travel_date=request.data['travel_date'], travel=request.data['travel'], location_number=request.data['location_number']) 
        if location:
            return Response(
                {"res": "No se puede reservar, puesto ya se encuentra ocupado para este viaje"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = LocationOperationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationDetailApiView(APIView):
    permission_classes = [IsSellerLocations]

    def get(self, request, id_location):
        try:
            serializer = LocationSerializer(Location.objects.get(id=id_location))
            return Response(serializer.data)
        except Location.DoesNotExist:
            return Response({'msg': "id not exist"},status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id_location):

        try:
            location = Location.objects.get(id=id_location)
            
            is_busy_location = Location.objects.filter(travel_date=location.travel_date) \
                                    .filter(travel=location.travel) \
                                    .filter(location_number=request.data['location_number'])
            if is_busy_location:
                return Response(
                    {"res": "No se puede realizar el cambio, puesto ya se encuentra ocupado para este viaje"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = LocationUpdateSerializer(location, request.data, partial = True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Location.DoesNotExist:
            return Response({'msg': "id not exist"},status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id_location):
        try:
            location = Location.objects.get(id=id_location)
            location.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Location.DoesNotExist:
            return Response({'msg': "id not exist"},status=status.HTTP_404_NOT_FOUND)


class TravelLocationsApiView(APIView):
    def post(self, request, id_travel):
        try:
            location = Location.objects.filter(travel__pk=id_travel,travel_date=request.data['date'])
            serializer = LocationNoAuthSerializer(location, many=True)
            return Response(serializer.data)
        except Location.DoesNotExist:
            return Response({'msg': "traveler not locations"},status=status.HTTP_404_NOT_FOUND)


class TravelerLocationsApiView(APIView):
    def get(self, request, id_card):
        try:
            location = Location.objects.filter(traveler=id_card, travel_date__gte=datetime.datetime.now())
            serializer = LocationNoAuthSerializer(location, many=True)
            return Response(serializer.data)
        except Location.DoesNotExist:
            return Response({'msg': "traveler not locations"},status=status.HTTP_404_NOT_FOUND)
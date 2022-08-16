from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import User
from .serializers import BusSerializer, JourneySerializer, TravelSerializer, ScheduleSerializer,\
    TravelOperationSerializer, JourneyOperationSerializer
from .permissions import IsAdminAndReadOnly
from travels.models import Bus, Journey, Schedule, Travel


class BusApiView(APIView):
    permission_classes = [IsAdminAndReadOnly]

    def get(self, request):
        serializer = BusSerializer(Bus.objects.filter(is_active=True), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BusSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusDetailApiView(APIView):
    permission_classes = [IsAdminAndReadOnly]

    def get(self, request, bus_plate):
        try:
            serializer = BusSerializer(Bus.objects.get(bus_plate=bus_plate))
            return Response(serializer.data)
        except Bus.DoesNotExist:
            return Response({'msg': "id not exist"},status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, bus_plate):
        try:
            bus = Bus.objects.get(bus_plate=bus_plate)
            serializer = BusSerializer(bus, request.data, partial = True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Bus.DoesNotExist:
            return Response({'msg': "id not exist"},status=status.HTTP_404_NOT_FOUND)


class JourneyApiView(APIView):
    permission_classes = [IsAdminAndReadOnly]

    def get(self, request):
        serializer = JourneySerializer(Journey.objects.filter(is_active=True), many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = JourneySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JourneyDetailApiView(APIView):
    permission_classes = [IsAdminAndReadOnly]

    def get(self, request, id_journey):
        try:
            serializer = JourneySerializer(Journey.objects.get(id=id_journey))
            return Response(serializer.data)
        except Journey.DoesNotExist:
            return Response({'msg': "id not exist"},status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id_journey):
        try:
            journey = Journey.objects.get(id=id_journey)
            serializer = JourneyOperationSerializer(journey, request.data, partial = True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Journey.DoesNotExist:
            return Response({'msg': "id not exist"},status=status.HTTP_404_NOT_FOUND)



class ScheduleApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ScheduleSerializer(Schedule.objects.filter(is_active=True), many=True)
        return Response(serializer.data)

class ScheduleJourneyApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id_journey):
        query = Travel.objects.filter(journey__pk=id_journey)
        scheduled = []
        for item in query:
            scheduled.append({
                "id":item.scheduled.id,
                "departure_time":item.scheduled.departure_time,
                "cases_closing":item.scheduled.cases_closing,
            })
        return Response(data=scheduled)


class TravelApiView(APIView):
    permission_classes = [IsAdminAndReadOnly]

    def get(self, request):
        serializer = TravelSerializer(Travel.objects.filter(is_active=True), many=True)
        for travels in serializer.data:
            travels.keke=9

        return Response(serializer.data)

    def post(self, request):
        serializer = TravelOperationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TravelDetailApiView(APIView):
    permission_classes = [IsAdminAndReadOnly]

    def get(self, request, id_travel):
        try:
            serializer = TravelSerializer(Travel.objects.get(id=id_travel))
            return Response(serializer.data)
        except Travel.DoesNotExist:
            return Response({'msg': "id not exist"},status=status.HTTP_404_NOT_FOUND)


    def patch(self, request, id_travel):
        try:
            travel = Travel.objects.get(id=id_travel)
            serializer = TravelOperationSerializer(travel, request.data, partial = True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Travel.DoesNotExist:
            return Response({'msg': "id not exist"},status=status.HTTP_404_NOT_FOUND)


class TravelDriverApiView(APIView):
    permission_classes = [IsAdminAndReadOnly]

    def get(self, request, id_driver):
        try:
            driver = User.objects.get(pk=id_driver)
            travels = Travel.objects.filter(driver=driver)
            serializer = TravelSerializer(travels,many=True)
            return Response(serializer.data)
        except Travel.DoesNotExist:
            return Response({'msg': "id not exist"},status=status.HTTP_404_NOT_FOUND)


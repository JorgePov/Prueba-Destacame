from django.urls import path 
from .views import BusApiView, BusDetailApiView, JourneyApiView, JourneyDetailApiView, ScheduleApiView, \
    TravelApiView, TravelDetailApiView, TravelDriverApiView, ScheduleJourneyApiView


urlpatterns = [
    path('buses', BusApiView.as_view()),
    path('buses/<str:bus_plate>', BusDetailApiView.as_view()),
    path('journeys', JourneyApiView.as_view()),
    path('journeys/<int:id_journey>', JourneyDetailApiView.as_view()),
    path('schedules', ScheduleApiView.as_view()),
    path('schedules/<int:id_journey>', ScheduleJourneyApiView.as_view()),
    path('travels', TravelApiView.as_view()),
    path('travels/<int:id_travel>', TravelDetailApiView.as_view()),
    path('driver/travels/<int:id_driver>', TravelDriverApiView.as_view())
]
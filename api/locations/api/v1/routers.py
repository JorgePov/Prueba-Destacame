from django.urls import path 
from .views import TravelerApiView, TravelerDetailApiView, LocationApiView, LocationDetailApiView, \
    TravelerLocationsApiView, TravelLocationsApiView


urlpatterns = [
    path('travelers', TravelerApiView.as_view()),
    path('travelers/<int:id_card>', TravelerDetailApiView.as_view()),
    path('locations', LocationApiView.as_view()),
    path('locations/<int:id_location>', LocationDetailApiView.as_view()),
    path('locations/travel/<int:id_travel>', TravelLocationsApiView.as_view()),
    path('locations/travelers/<int:id_card>', TravelerLocationsApiView.as_view()),
]
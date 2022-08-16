from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterView, UserView, UserAdminView, UserDriverView,AllUserView

urlpatterns = [
    path('users/signup', RegisterView.as_view()),
    path('users/login', TokenObtainPairView.as_view()),
    path('users', UserView.as_view()),
    path('users/<int:user_id>', UserAdminView.as_view()),
    path('drivers', UserDriverView.as_view()),
    path('employes', AllUserView.as_view()),
    
]

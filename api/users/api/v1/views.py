from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .serializers import UserResgisterSerializer, UserSerializer, \
    UserUpdateSerializer, DriverSerializer
from users.models import User

class RegisterView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = UserResgisterSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserDriverView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        serializer = DriverSerializer(User.objects.filter(is_driver=True), many=True)
        return Response(serializer.data)

class AllUserView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        serializer = DriverSerializer(User.objects.all(), many=True)
        return Response(serializer.data)


class UserAdminView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserUpdateSerializer(user, request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'msg': "id not exist"},status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        user = User.objects.get(id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


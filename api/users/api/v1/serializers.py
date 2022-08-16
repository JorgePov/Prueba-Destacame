from rest_framework import serializers
from users.models import User

class UserResgisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'full_name', 'age', 'id_card', 'is_driver', 'is_seller')

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        validated_data['full_name'] = f'%s %s' % ( validated_data['first_name'], validated_data['last_name'])
        validated_data['username'] = validated_data['first_name']
        instance  = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','first_name','last_name', 'full_name', 'is_driver', 'is_seller', 'is_staff')

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'full_name', 'age', 'id_card', 'is_driver', 'is_seller', 'is_staff')
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'age','first_name', 'last_name', 'is_driver', 'is_seller', 'is_staff')
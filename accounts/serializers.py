from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
 
User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    password = serializers.CharField(max_length=300, required=False)
    
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__'
        

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=300, required=False)
    class Meta():
        model = User
        fields = '__all__'
        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=300)
from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            
        ]
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        return make_password(value)



class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class MailAndOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp= serializers.IntegerField()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
        
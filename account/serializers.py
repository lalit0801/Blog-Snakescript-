from rest_framework import serializers
from .models import *
from utils.utils import AccountUtils


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    

class MailVerificationOTPSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MailVerificationOTP
        fields = '__all__'
        read_only_fields = ['id', 'updated_at']
        
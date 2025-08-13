from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer
from authentication.models import *


class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD


class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    new_password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('__all__')
        read_only_fields = ('id', 'is_active', 'is_superuser',
                            'is_staff', 'user_permissions', 'date_joined', 'last_login')
        extra_kwargs = {'password': {'write_only': True}}


class ProfileEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','email')
        read_only_fields = ('id',)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('__all__')
        read_only_fields = ('id', 'is_active', 'is_superuser',
                            'is_staff', 'user_permissions', 'date_joined', 'last_login','groups')
        extra_kwargs = {'password': {'write_only': True}}


class UserExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','first_name','last_name','gender','username','email','phone_number')
        read_only_fields = ('id','username','email','recorded_by','recorded_at')


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','username','email')
        read_only_fields = ('id','username','email',)


class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    subject = serializers.CharField(max_length=150)
    body = serializers.CharField(max_length=512)


class OTPEmailSerializer(serializers.Serializer):
    staff_email = serializers.CharField(max_length=150)
    staff_name = serializers.CharField(max_length=150)
    system_name = serializers.CharField(max_length=150)
    otp_code = serializers.CharField(max_length=150)



class HtmlEmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    subject = serializers.CharField(max_length=150)
    message = serializers.CharField()


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)
    system = serializers.CharField(max_length=150)



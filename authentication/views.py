from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http.response import JsonResponse
from django.contrib.gis.geos import GEOSGeometry

import json
import requests
from django.utils import timezone
from rest_framework import pagination
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import *
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import *
from django.db.models import Q
from datetime import date, timedelta
from rest_framework.settings import api_settings
from rest_framework import filters
import django_filters.rest_framework
from django_filters import DateRangeFilter,DateFilter

from authentication.serializers import *
from authentication.models import *
from authentication.utils import generate_unique_number
from authentication.service import *
from app.models import *

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class getUserByEmail(APIView):

    serializer_class = ProfileSerializer

    def get(self, request, email):
        if '@' in email:
        	user = Profile.objects.get(email=email)
        else:
        	user = Profile.objects.get(username=email)
        serializer = ProfileSerializer(user, many=False)
        return JsonResponse(serializer.data, safe=False)


class profileSearch(django_filters.FilterSet):

    exclude_id = django_filters.CharFilter(method='filter_exclude_id')

    class Meta:
        model = Profile
        fields = {'id': ['exact','in'],'username': ['exact']}

    def filter_exclude_id(self, queryset, name, value):
        try:
            ids = [int(id) for id in value.split(',')]
            return queryset.exclude(id__in=ids)
        except ValueError:
            return queryset


class ProfileFilter(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = profileSearch
    search_fields = ['first_name','last_name', 'email', 'username']
    ordering_fields = ['id', 'first_name','username']
    ordering = ['-id']


class userList(ListAPIView):
    queryset = Profile.objects.all().order_by('-id')
    serializer_class = UserListSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'username']


class profileAdd(CreateAPIView):

    serializer_class = ProfileSerializer
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            password = make_password(self.request.data.get("password"))
            serializer.save(password=password)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AuthToken(CreateAPIView):

    serializer_class = AuthSerializer

    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if '@' in data['username']:
                profile = Profile.objects.filter(email=data['username'], is_active=True)
            else:
                profile = Profile.objects.filter(username=data['username'], is_active=True)
            if profile:
                hr = requests.get('http://192.168.101.141:5051/gateway/api/staff/data/'+data['username'])
                hr_data=None
                if hr:
                    hr_data = json.loads(hr.text)

                user = Profile.objects.get(authuser_ptr=profile[0].id)
                if user.is_active:
                    system = System.objects.filter(code=data['system'].lower(), is_active=True)
                    if system:
                        user_system = SystemUser.objects.filter(system=system[0], user=user, is_active=True)
                        role = UserRole.objects.filter(system=system[0], user=user)
                        roles = []
                        for rl in role:
                            ro = Role.objects.get(id=rl.role.id)
                            rll = {'name': ro.name, 'description': ro.description}
                            roles.append(rll)
                        if user_system:
                            auth = authenticate(username=data['username'], password=data['password'])
                            if auth:
                                refresh = RefreshToken.for_user(auth)
                                token = {
                                    'access': str(refresh.access_token),
                                    'refresh': str(refresh),
                                }

                                user_data = {
                                    'id': user.id,
                                    'first_name': user.first_name,
                                    'last_name': user.last_name,
                                    'gender': user.gender,
                                    'email': user.email,
                                    'phone_number': user.phone_number,
                                    'is_first_login': user.is_first_login,
                                    'username': user.username,
                                    'branch_id': hr_data['active_departments'][0]['branch']['id'],
                                    'branch_code': hr_data['active_departments'][0]['branch']['branch_code'],
                                    'branch_name': hr_data['active_departments'][0]['branch']['branch_name'],
                                    'department_id': hr_data['active_departments'][0]['department']['id'],
                                    'department_name': hr_data['active_departments'][0]['department']['department_name'],
                                    'position': hr_data['active_departments'][0]['position']['id'],
                                }

                                system_data = {
                                    'id': system[0].id,
                                    'code': system[0].code,
                                    'name': system[0].name,
                                    'description': system[0].description,
                                    'roles': roles,
                                }
                                
                                response_data = {
                                    'user': user_data,
                                    'system': system_data,
                                    'token': token,
                                }
                                user_system.update(last_access=timezone.now())
                                profile.update(last_login=timezone.now())
                                return Response(response_data, status=status.HTTP_200_OK)
                            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
                        return Response({"error": "You are not allowed to use this system"}, status=status.HTTP_400_BAD_REQUEST)
                    return Response({"error": "System is not used"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"error": "You are not an active user"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "You are not an active user"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)



class activateUser(APIView):

    def post(self, request, pk):
        user = Profile.objects.get(authuser_ptr=pk)
        if user.is_active == True:
            Profile.objects.filter(authuser_ptr=pk).update(is_active=False)
        else:
            Profile.objects.filter(authuser_ptr=pk).update(is_active=True)
        return Response({""}, status=status.HTTP_200_OK)


class authoriseUser(APIView):

    def post(self, request, pk):
        user = Profile.objects.filter(authuser_ptr=pk).update(is_first_login=False)
        return Response({""}, status=status.HTTP_200_OK)



class changePassword(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = get_user_model()
    # permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetView(APIView):

    serializer_class = ResetPasswordSerializer()

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            new_password = serializer.validated_data['new_password']

            try:
                user = Profile.objects.get(username=username)
            except Profile.DoesNotExist:
                return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # validate_password(new_password, user)
                user.set_password(new_password)
                user.save()
                Profile.objects.filter(username=username).update(is_first_login=True)
                return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
            except DjangoValidationError as e:
                return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileEmailChange(CreateAPIView):

    serializer_class = ProfileEmailSerializer

    def put(self, request, pk):
        instance = Profile.objects.get(id=pk)
        serializer = ProfileEmailSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SendEmail(CreateAPIView):

    serializer_class = EmailSerializer

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
           validated_data = serializer.validated_data
           request_number = generate_unique_number()
           token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRJRCI6IjE4OWU1NzkzLWFhYjYtNGFhNy1iM2RmLWUxYzMxZTg3MTdmNCJ9.eQJQ76SQ1fJ4iJ7mr8D6m4ursO6Glbel3U1GYBNKWXs"
           request_headers = {'X-Request-Id':request_number,'Authorization':token}
           send_data = {"email": validated_data['email'],"subject": validated_data['subject'],"body": validated_data['body']}
           resp = requests.post('http://172.20.1.13:2073/api/v1/send-email', headers=request_headers, json=send_data)
           if resp:
               return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SendOTPEmail(CreateAPIView):

    serializer_class = OTPEmailSerializer

    def post(self, request):
        serializer = OTPEmailSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            send_otp_email(validated_data['staff_email'], validated_data['staff_name'], validated_data['system_name'], validated_data['otp_code'])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SendHtmlEmail(CreateAPIView):

    serializer_class = HtmlEmailSerializer

    def post(self, request):
        serializer = HtmlEmailSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            send_html_email(validated_data['email'],validated_data['subject'],validated_data['message'])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateBalkUser(APIView):

    def post(self, request):
        hr = requests.get('http://192.168.101.141:5051/gateway/api/staff/list')
        if hr:
            hr_data = json.loads(hr.text)
            for hr_d in hr_data:
                user_av = Profile.objects.filter(username = hr_d['staff_opf'])
                if user_av:
                    print('available')
                else:
                    print(hr_d['staff_opf'])
        return Response({""}, status=status.HTTP_200_OK)





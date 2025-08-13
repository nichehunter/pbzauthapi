from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http.response import JsonResponse
from django.contrib.gis.geos import GEOSGeometry

import json
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

from app.serializers import *
from app.models import *

# Create your views here.

#===================================== system =========================================================
class systemSearch(django_filters.FilterSet):

    exclude_id = django_filters.CharFilter(method='filter_exclude_id')

    class Meta:
        model = System
        fields = {
            'id': ['exact','in'],
            'code': ['exact',],
            'name': ['exact']
        }


    def filter_exclude_id(self, queryset, name, value):
        try:
            ids = [int(id) for id in value.split(',')]
            return queryset.exclude(id__in=ids)
        except ValueError:
            return queryset


class SystemAdd(CreateAPIView):

    serializer_class = SystemSerializer
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = SystemSerializer(data=request.data)
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SystemList(ListAPIView):
    queryset = System.objects.all()
    serializer_class = SystemSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = systemSearch
    search_fields = ['code','name','url']
    ordering_fields = ['id','code', 'name','url']
    ordering = ['-id']


#===================================== system =========================================================
class roleSearch(django_filters.FilterSet):

    class Meta:
        model = Role
        fields = {'name': ['exact','in'],'system__id': ['exact','in']}


class RoleAdd(CreateAPIView):

    serializer_class = RoleSerializer

    def post(self, request):
        serializer = RoleSerializer(data=request.data, many=True)
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleList(ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleListSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = roleSearch
    search_fields = ['name','system__name','system__code']
    ordering_fields = ['id', 'name','system__code']
    ordering = ['-id']



#===================================== system user =========================================================
class systemUserSearch(django_filters.FilterSet):

    class Meta:
        model = SystemUser
        fields = {'id': ['exact','in'],'system__id': ['exact','in'],'user__id': ['exact','in']}




class SystemUserAdd(CreateAPIView):

    serializer_class = SystemUserSerializer

    def post(self, request):
        serializer = SystemUserSerializer(data=request.data, many=True)
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SystemUserList(ListAPIView):
    queryset = SystemUser.objects.all()
    serializer_class = SystemUserListSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = systemUserSearch
    search_fields = ['system__name','user__username','user__first_name']
    ordering_fields = ['id','system__code','system__name','user__username','user__first_name']
    ordering = ['-id']


class ActivateUserSystem(APIView):

    def post(self, request, pk):
        system = SystemUser.objects.get(id=pk)
        if system.is_active == True:
            SystemUser.objects.filter(id=pk).update(is_active=False)
        else:
            SystemUser.objects.filter(id=pk).update(is_active=True)
        return Response({""}, status=status.HTTP_200_OK)

#===================================== system =========================================================
class userRoleSearch(django_filters.FilterSet):

    class Meta:
        model = UserRole
        fields = {'role__id': ['exact','in'],'system__id': ['exact','in'],'user__id': ['exact','in']}


class UserRoleAdd(CreateAPIView):

    serializer_class = UserRoleSerializer

    def post(self, request):
        serializer = UserRoleSerializer(data=request.data, many=True)
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRoleList(ListAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleListSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = userRoleSearch
    search_fields = ['role__name','system__name','user__username']
    ordering_fields = ['id', 'role__name','system__name','user__username']
    ordering = ['-id']


class UserRoleRemove(APIView):

    serializer_class = UserRoleRemoveSerializer

    def delete(self, request):
        serializer = UserRoleRemoveSerializer(data=request.data, many=True)
        if serializer.is_valid():            
            for x in serializer.validated_data:
                user = x['user']
                role = x['role']
                system = x['system']
                UserRole.objects.filter(user=user, role=role, system=system).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#===================================== system =========================================================
class userLogsSearch(django_filters.FilterSet):

    class Meta:
        model = UserLogs
        fields = {'system__id': ['exact','in'],'user__id': ['exact','in'],'recorded_at': ['range']}


class UserLogsAdd(CreateAPIView):

    serializer_class = UserLogsSerializer

    def post(self, request):
        serializer = UserLogsSerializer(data=request.data)
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogsList(ListAPIView):
    queryset = UserLogs.objects.all()
    serializer_class = UserLogsListSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = userLogsSearch
    search_fields = ['system__name','user__username']
    ordering_fields = ['id','system__name','user__username']
    ordering = ['-id']  

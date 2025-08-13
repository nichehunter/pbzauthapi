from rest_framework import fields, serializers
import json
import datetime
from app.models import *
from authentication.models import Profile

#===================================== profile =========================================================
class UserExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','first_name','last_name','gender','username','email','phone_number')
        read_only_fields = ('id','username')

#===================================== system =========================================================
class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ('__all__')
        read_only_fields = ('id',)


class SystemExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ('id','code','name','url','description')
        read_only_fields = ('id',)

#===================================== roles =========================================================
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('__all__')
        read_only_fields = ('id',)


class RoleListSerializer(serializers.ModelSerializer):
    system = SystemExportSerializer(read_only=True)
    class Meta:
        model = Role
        fields = ('__all__')
        read_only_fields = ('id',)


class RoleExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id','name')
        read_only_fields = ('id',)

#===================================== system user =========================================================
class SystemUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemUser
        fields = ('__all__')
        read_only_fields = ('id',)


class SystemUserListSerializer(serializers.ModelSerializer):
    system = SystemExportSerializer(read_only=True)
    user = UserExportSerializer(read_only=True)
    class Meta:
        model = SystemUser
        fields = ('__all__')
        read_only_fields = ('id',)


#===================================== roles =========================================================
class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ('__all__')
        read_only_fields = ('id',)


class UserRoleListSerializer(serializers.ModelSerializer):
    system = SystemExportSerializer(read_only=True)
    role = RoleExportSerializer(read_only=True)
    user = UserExportSerializer(read_only=True)
    class Meta:
        model = UserRole
        fields = ('__all__')
        read_only_fields = ('id',)


class UserRoleRemoveSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    role = serializers.IntegerField()
    system = serializers.IntegerField()

#===================================== logs =========================================================
class UserLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogs
        fields = ('__all__')
        read_only_fields = ('id',)


class UserLogsListSerializer(serializers.ModelSerializer):
    system = SystemExportSerializer(read_only=True)
    user = UserExportSerializer(read_only=True)
    class Meta:
        model = UserLogs
        fields = ('__all__')
        read_only_fields = ('id',)
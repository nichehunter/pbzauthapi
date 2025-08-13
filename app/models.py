from django.db import models
from authentication.models import *

# Create your models here.

class NameField(models.CharField):

    def get_prep_value(self, value):
        return str(value).lower()

class System(models.Model):
    code = NameField(max_length=100, unique=True)
    name = NameField(max_length=100, unique=True)
    url = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    recorded_by = models.ForeignKey(AuthUser, on_delete = models.RESTRICT)
    recorded_at = models.DateTimeField(auto_now_add = True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "System"
        verbose_name_plural = "Systems" 


class Role(models.Model):
    name = NameField(max_length=100)
    description = models.TextField(blank=True, null=True)
    system = models.ForeignKey(System, on_delete = models.RESTRICT)
    recorded_by = models.ForeignKey(AuthUser, on_delete = models.RESTRICT)
    recorded_at = models.DateTimeField(auto_now_add = True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles" 
        unique_together = ('name', 'system')


class SystemUser(models.Model):
    user = models.ForeignKey(Profile, on_delete = models.RESTRICT, related_name ="system_user")
    system = models.ForeignKey(System, on_delete = models.RESTRICT)
    last_access = models.DateTimeField(blank = True, null=True)
    is_active = models.BooleanField(default=True)
    recorded_by = models.ForeignKey(AuthUser, on_delete = models.RESTRICT)
    recorded_at = models.DateTimeField(auto_now_add = True, null=True)

    def __str__(self):
        return self.system.name
    
    class Meta:
        verbose_name = "System User"
        verbose_name_plural = "System Users" 
        unique_together = ('user', 'system')


class UserRole(models.Model):
    user = models.ForeignKey(Profile, on_delete = models.RESTRICT, related_name ="user")
    role = models.ForeignKey(Role, on_delete = models.RESTRICT)
    system = models.ForeignKey(System, on_delete = models.RESTRICT)
    recorded_by = models.ForeignKey(AuthUser, on_delete = models.RESTRICT)
    recorded_at = models.DateTimeField(auto_now_add = True, null=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "User Role"
        verbose_name_plural = "User Roles" 
        unique_together = ('user', 'role', 'system')


class UserLogs(models.Model):
    user = models.ForeignKey(Profile, on_delete = models.RESTRICT)
    activity = NameField(max_length=512)
    system = models.ForeignKey(System, on_delete = models.RESTRICT)
    recorded_at = models.DateTimeField(auto_now_add = True, null=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "User Logs"
        verbose_name_plural = "User Logs" 


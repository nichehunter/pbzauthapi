from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from app.views import *

urlpatterns = [
    path('system', SystemAdd.as_view()),
    path('system/list', SystemList.as_view()),
    path('role', RoleAdd.as_view()),
    path('role/list', RoleList.as_view()),
    path('system-user', SystemUserAdd.as_view()),
    path('system-user/list', SystemUserList.as_view()),
    path('system-user/activate/<int:pk>', ActivateUserSystem.as_view()),
    path('user-role', UserRoleAdd.as_view()),
    path('user-role/list', UserRoleList.as_view()),
    path('user-role/remove', UserRoleRemove.as_view()),
    path('user-logs', UserLogsAdd.as_view()),
    path('user-logs/list', UserLogsList.as_view()),
]
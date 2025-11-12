from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import *

urlpatterns = [
    path('user', profileAdd.as_view()),
    path('user/email/<int:pk>', ProfileEmailChange.as_view()),
    path('user/password/<int:pk>', changePassword.as_view()),
    path('user/reset_password', PasswordResetView.as_view()),
    path('user/authorise/<int:pk>', authoriseUser.as_view()),
    path('user/activate/<int:pk>', activateUser.as_view()),
    path('user/list', ProfileFilter.as_view()),
    # path('user/list', userList.as_view()),
    path('user/<str:email>', getUserByEmail.as_view()),
    path('auth/token', AuthToken.as_view()),
    path('token/verify', VerifyAuthToken.as_view()),
    path('token/obtain', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('send-email', SendEmail.as_view()),
    path('send-otp-email', SendOTPEmail.as_view()),
    path('send-normal-email', SendHtmlEmail.as_view()),
    path('balk-user', CreateBalkUser.as_view()),
]
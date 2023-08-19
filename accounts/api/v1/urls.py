from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from rest_framework.authtoken.views import ObtainAuthToken


app_name = 'api-v1'


urlpatterns = [
    # registration
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),

    # login token
    path('token/login/', views.CustomObtainAuthToken.as_view(), name='token-login'),
    path('token/logout/', views.CustomDiscardAuthToken.as_view(), name='token-logout'),

    # login jwt
    # path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    # path('jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/create/', views.JWTObtainPairTokenApiView.as_view()),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
    
    # change password
    path('change-password/', views.ChangePasswordApiView.as_view(), name='change-password'),

    #profile
    path('profile/', views.ProfileApiView.as_view(), name='profile'),

    # email
    path("test-email", views.TestEmailSend.as_view(), name="test-email"),
    # activation
    path("activation/confirm/<str:token>", views.ActivationApiView.as_view(), name="activation"),
    # resend activation
    path("activation/resend/", views.ActivationResendApiView.as_view(), name="activation-resend"),

    path('register/email-verify/', views.VerifyEmailApiView.as_view(), name='email_verify'),
    path('reset-password/validate-token/', views.PasswordResetTokenValidateApiView.as_view(),name='reset-password-validate'),
    path('reset-password/set-password/', views.PasswordResetSetNewApiView.as_view(),name='reset-password-confirm'),
]

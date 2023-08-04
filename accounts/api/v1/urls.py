from django.urls import path, include
from . import views

urlpatterns = [
    # registration
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),
]

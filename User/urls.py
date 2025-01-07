from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.user_registration, name='registration'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('log-in/', views.log_in, name="log_in")
]
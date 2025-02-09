from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.userProfile, name='profile'),
    path('registration/', views.user_registration, name='registration'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('log-in/', views.logIn, name="log_in"),
    path('log-out/', views.log_out, name="log_out"),
]

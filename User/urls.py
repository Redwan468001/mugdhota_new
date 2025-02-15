from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.userDashboard, name='user_dashboard'),
    path('all-content/<str:username>/', views.user_total_content, name='user_total_content'),
    path('published-content/<str:username>/', views.user_published_content, name='user_published_content'),
    path('pending-content/<str:username>/', views.user_pending_content, name='user_pending_content'),
    path('refuge-content/<str:username>/', views.user_refuge_content, name='user_refuge_content'),
    path('registration/', views.user_registration, name='registration'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('log-in/', views.logIn, name="log_in"),
    path('log-out/', views.log_out, name="log_out"),
]

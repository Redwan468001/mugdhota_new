from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:slug>', views.singlepost, name='universalsinglepost'),
]
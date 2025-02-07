from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.artandliterature, name='artandliterature'),
    path('<str:category>/', views.singlecategory, name='singlecategory'),
    path('<slug:slug>/', views.single_post, name='single_post'),
]
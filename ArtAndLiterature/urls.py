from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.artandliterature, name='artandliterature'),
    path('upload-content/', views.uploadArtAndLiterature, name='upload_content'),
    path('<str:slug>/', views.single_post, name='single_post'),
    path('category/<str:category>/', views.singlecategory, name='singlecategory'),
]



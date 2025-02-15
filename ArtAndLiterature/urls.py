from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.artandliterature, name='artandliterature'),
    path('upload-content/', views.uploadArtAndLiterature, name='upload_content'),
    path('edit-content/<str:slug>/', views.editContent, name='edit_art_content'),
    path('<str:slug>/', views.single_post, name='single_post'),
    path('delete/<str:slug>/', views.deletecontent, name='deletecontent'),
    path('category/<str:category>/', views.singlecategory, name='singlecategory'),
]



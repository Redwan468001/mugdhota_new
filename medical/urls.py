from django.urls import path
from . import views

urlpatterns = [
    path('', views.medicalinsight, name='medicalinsight'),
    path('upload-content/', views.uploadmedicalcnt, name='upload_content_medi'),
    path('<str:slug>/', views.single_post, name='single_post_medi'),
    path('category/<str:category>/', views.singlecategory, name='singlecategory_medi'),
]
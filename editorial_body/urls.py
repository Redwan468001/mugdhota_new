from django.urls import path
from . import views

urlpatterns = [
    path('editorial-dashboard/<str:username>/', views.management_dashboard, name='management_dashboard'),
    path('editorial-edit-content/<str:slug>/', views.edituseruploadedpost, name='editorial_edit_content'),
    path('user-uploaded-all-content/', views.user_uploaded_all_content, name='user_uploaded_all_content'),
    path('user-published-content/', views.user_published_content, name='user_published_content'),
    path('user-pending-content/', views.user_pending_content, name='user_pending_content'),
    path('user-refuged-content/', views.user_refuged_content, name='user_refuged_content'),
]
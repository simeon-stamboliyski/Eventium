from django.urls import path
from profiles import views

urlpatterns = [
    path('create/', views.profile_create, name='profile-create'),
    path('details/', views.profile_details, name='profile-details'),
    path('<int:pk>/edit/', views.profile_edit, name='profile-edit'),
    path('<int:pk>/delete/', views.profile_delete, name='profile-delete'),
]
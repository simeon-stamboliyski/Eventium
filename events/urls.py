from django.urls import path
from events import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event-create'),
    path('<int:event_pk>/details/', views.event_details, name='event-details'),
    path('<int:event_pk>/edit/', views.event_edit, name='event-edit'),
    path('<int:event_pk>/delete/', views.event_delete, name='event-delete'),
]
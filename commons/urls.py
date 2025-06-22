from django.urls import path
from commons import views as common_views

urlpatterns = [
    path('', common_views.index, name='index'),
]
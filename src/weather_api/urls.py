# clima_backend/src/weather_api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.get_weather, name='get_weather'),
]
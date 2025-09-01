# clima_backend/src/clima_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Incluye las URLs de tu aplicación weather_api
    path('api/', include('weather_api.urls')),
]
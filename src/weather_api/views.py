# clima_backend/src/weather_api/views.py

import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Obtener la API Key desde settings.py (que a su vez la carga desde .env)
# Importante: En un proyecto grande, se accedería directamente desde django.conf.settings
# Para simplicidad inicial, podemos cargarla aquí, pero el mejor lugar es settings.py
from django.conf import settings

@api_view(['GET']) # Esto indica que esta vista solo acepta peticiones GET
def get_weather(request):
    city = request.GET.get('city') # Obtiene la ciudad de los parámetros de la URL (?city=BuenosAires)

    if not city:
        return Response(
            {"error": "Debe proporcionar el nombre de una ciudad."},
            status=status.HTTP_400_BAD_REQUEST
        )

    api_key = settings.OPENWEATHERMAP_API_KEY # Usamos la API Key de settings.py
    if not api_key:
        return Response(
            {"error": "La API Key de OpenWeatherMap no está configurada."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # URL de la API de OpenWeatherMap
    # 'q': ciudad, 'appid': tu clave, 'units': métricas (Celsius), 'lang': idioma (español)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es"

    try:
        response = requests.get(url)
        response.raise_for_status() # Lanza una excepción para errores HTTP (4xx o 5xx)
        weather_data = response.json()

        # Extraer solo los datos relevantes
        extracted_data = {
            "city": weather_data.get("name"),
            "country": weather_data.get("sys", {}).get("country"),
            "temperature": weather_data.get("main", {}).get("temp"),
            "feels_like": weather_data.get("main", {}).get("feels_like"),
            "description": weather_data.get("weather", [{}])[0].get("description"),
            "icon": weather_data.get("weather", [{}])[0].get("icon"),
            "humidity": weather_data.get("main", {}).get("humidity"),
            "wind_speed": weather_data.get("wind", {}).get("speed"),
        }
        return Response(extracted_data, status=status.HTTP_200_OK)

    except requests.exceptions.RequestException as e:
        # Manejo de errores de conexión o HTTP
        return Response(
            {"error": f"Error al conectar con la API del clima: {e}"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE # Servicio no disponible
        )
    except Exception as e:
        # Manejo de cualquier otro error inesperado
        return Response(
            {"error": f"Ocurrió un error inesperado: {e}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
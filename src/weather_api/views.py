from rest_framework.views import APIView
from django.http import JsonResponse
import requests
import os

class WeatherView(APIView):
    def get(self, request):
        city = request.GET.get('city', 'Buenos Aires')
        api_key = os.getenv('OPENWEATHER_API_KEY')

        if not api_key:
            return JsonResponse({'error': 'La clave de la API no está configurada.'}, status=500)

        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es'

        try:
            response = requests.get(url)

            # Debugging: Imprime el estado y el texto de la respuesta en la terminal
            print(f"URL de la API: {url}")
            print(f"Estado de la respuesta de la API: {response.status_code}")
            print(f"Texto de la respuesta de la API: {response.text}")

            response.raise_for_status()  # Lanza un error si la solicitud no fue exitosa
            data = response.json()

            weather_data = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
            }

            return JsonResponse(weather_data)

        except requests.exceptions.HTTPError as e:
            # Captura errores HTTP específicos (401, 404, etc.)
            return JsonResponse({'error': f'Error de la API: {e}'}, status=500)
        except requests.exceptions.RequestException as e:
            # Captura cualquier otro error de conexión
            return JsonResponse({'error': f'Error de conexión: {e}'}, status=500)
        except Exception as e:
            # Captura cualquier otro error inesperado
            return JsonResponse({'error': f'Ocurrió un error inesperado: {e}'}, status=500)

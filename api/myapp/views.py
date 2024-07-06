from django.http import JsonResponse
import requests
from django.conf import settings

def get_location_and_weather(ip_address):
    try:
        location_response = requests.get(f'http://ipinfo.io/{ip_address}/json')
        location_response.raise_for_status()
        location_data = location_response.json()
        city = location_data.get('city', 'unknown')
    except requests.RequestException as e:
        city = 'unknown'
    
    try:
        api_key = settings.API_KEY
        weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric')
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        temperature = weather_data['main']['temp'] if 'main' in weather_data else 'unknown'
    except requests.RequestException as e:
        temperature = 'unknown'
    
    return city, temperature

def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Guest')
    client_ip = request.META.get('REMOTE_ADDR')

    city, temperature = get_location_and_weather(client_ip)

    response = {
        'client_ip': client_ip,
        'location': city,
        'greeting': f'Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {city}.'
    }

    return JsonResponse(response)

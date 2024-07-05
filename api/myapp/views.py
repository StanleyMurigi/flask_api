from django.http import JsonResponse
import requests
from django.conf import settings

def get_location_and_weather(ip_address):
    location_response = requests.get(f'http://ipinfo.io/{ip_address}/json')
    location_data = location_response.json()
    city = location_data.get('city', 'unknown')

    api_key = settings.API_KEY
    weather_response = requests.get(f'http://api.openweather.org/data/2.5/weather?q={city}&appid={api_key}&units=metric')
    weather_data = weather_response.json()
    temperature = weather_data['main']['temp'] if 'main' in weather_data else 'unknown'

    return city, temperature


def hello(requests):
    visitor_name = requests.GET.get('visitor_name', 'Guest')
    client_ip = requests.META.get('REMOTE_ADDR')

    city, temperature = get_location_and_weather(client_ip)

    response = {
        'client_ip': client_ip,
        'location': city,
        'greeting': f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}'
    }

    return JsonResponse(response)
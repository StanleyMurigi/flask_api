from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_location(ip):
    response = requests.get(f"https://ipapi.co/{ip}/json/")
    if response.status_code == 200:
        return response.json()
    return None

def get_weather(city):
    api_key = '6d1c78472fc512e620890599d6cf6afa'
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
    if response.status_code == 200:
        return response.json()
    return None

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Visitor')
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    location = get_location(client_ip)
    
    if location:
        city = location.get('city', 'Unknown')
        weather = get_weather(city)
        if weather:
            temp = weather['main']['temp']
            greeting = f"Hello, {visitor_name}! The temperature is {temp} degrees Celsius in {city}."
        else:
            greeting = f"Hello, {visitor_name}! Weather information is not available for {city}."
    else:
        city = "Unknown"
        greeting = f"Hello, {visitor_name}!"

    response = {
        "client_ip": client_ip,
        "location": city,
        "greeting": greeting
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)


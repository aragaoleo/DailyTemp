from dotenv import load_dotenv
import os
import requests
load_dotenv()

api_key = os.getenv("api_key")


def get_location(city, state):
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}'
    response = requests.get(url)

    data = response.json()
    for location in data:
        if location.get("state") == state:
            return {"City": location["name"],"state": location["state"],"country": location["country"],"lat": location["lat"], "lon": location["lon"]}
        
    print("Erro de digitação")
    return None

location = get_location(city="Aracaju",state="Sergipe")
print(location)


def get_weather(city,state):

    
    if location: 

        lat = location['lat']
        lon = location['lon']

        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt_br'
        response = requests.get(url)
        weather_data = response.json()
        return weather_data
    else:
        print('Erro ao encontrar localização')
        return None

weather = get_weather(city='Aracaju', state='Sergipe')
print(weather)
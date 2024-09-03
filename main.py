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
            return {"lat": location["lat"], "lon": location["lon"], "country": location["country"], "state": location["state"]}
        
    print("Erro de digitação")
    return None

location_data = get_location(city="Aracaju",state="Sergipe")
print(location_data)
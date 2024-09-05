from dotenv import load_dotenv
import os
import requests
import pandas as pd
from datetime import datetime
import pytz
load_dotenv()

api_key = os.getenv("api_key")

city = input("digite a cidade: ")
state = input("digite o estado: ")

def get_location(city, state):
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}'
    response = requests.get(url)

    data = response.json()
    for location in data:
        if location.get("state") == state:
            return {"lat": location["lat"], "lon": location["lon"]}
        
    print("Erro de digitação")
    return None

location = get_location(city,state)

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

weather = get_weather(city,state)
if weather is not None:

    timestamp = weather.get('dt', None)  # timestamp do clima
    if timestamp:
        # Converter o timestamp UTC para uma data e hora em UTC
        dt_utc = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
        
        # Converter o horário UTC para o horário local
        local_tz = pytz.timezone('America/Sao_Paulo')  # Ajuste para o fuso horário desejado
        dt_local = dt_utc.astimezone(local_tz)
        
        # Formatar a data e hora local
        dt_txt = dt_local.strftime('%Y-%m-%d %H:%M:%S')

    temp = weather['main']['temp']
    feels_like = weather['main']['feels_like']
    temp_min = weather['main']['temp_min']
    temp_max = weather['main']['temp_max']
    pressure = weather['main']['pressure']
    humidity = weather['main']['humidity']
    weather_desc = weather['weather'][0]['description']
    wind_speed = weather['wind']['speed']
    
    rows = [{
        'Hora': dt_txt,
        'Temperatura': temp,
        'Sensação térmica': feels_like,
        'Pressão atmosférica': pressure,
        'Humidade': humidity,
        'Descrição do tempo': weather_desc,
        'Velocidade do vento': wind_speed*3.6,
    }]

    dfWeather = pd.DataFrame(rows)
    print(dfWeather)
else:
    print("Erro: não foi possível obter os dados do clima atual.")

def get_forecast(city,state):
    if location: 

        lat = location['lat']
        lon = location['lon']

        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt_br'
        response = requests.get(url)
        forecast_data = response.json()
        return forecast_data
    else:
        print('Erro ao encontrar localização')
        return None

forecast = get_forecast(city,state)

if forecast is not None and 'list' in forecast:
    forecast_list = forecast['list']

    rows = []
    for entry in forecast_list:
        dt_txt = entry['dt_txt']
        temp = entry['main']['temp']
        feels_like = entry['main']['feels_like']
        temp_min = entry['main']['temp_min']
        temp_max = entry['main']['temp_max']
        pressure = entry['main']['pressure']
        humidity = entry['main']['humidity']
        weather_desc = entry['weather'][0]['description']
        wind_speed = entry['wind']['speed']
        pop = entry.get('pop', None)
        
        rows.append({
            'Data e hora': dt_txt,
            'Temperatura': temp,
            'Sensação térmica': feels_like,
            'Temperatura mínima': temp_min,
            'Temperatura máxima': temp_max,
            'Pressão atmosférica': pressure,
            'Umidade': humidity,
            'Descrição do tempo': weather_desc,
            'Velocidade do vento': wind_speed*3.6,
            'Chance de chuva': pop*100
        })

    dfForecast = pd.DataFrame(rows)


    print(dfForecast)
else:
    print("Erro: não foi possível obter os dados de previsão do tempo.")
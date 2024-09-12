from dotenv import load_dotenv
import os
import requests
import pandas as pd
from datetime import datetime
import pytz
from collections import Counter
import math
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

location = get_location(city, state)

def get_weather(city, state):
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

weather = get_weather(city, state)
if weather is not None:

    timestamp = weather.get('dt', None)
    if timestamp:
        dt_utc = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
        local_tz = pytz.timezone('America/Sao_Paulo')
        dt_local = dt_utc.astimezone(local_tz)
        dt_txt = dt_local.strftime('%H:%M') 

    temp = math.ceil(weather['main']['temp'])
    feels_like = math.ceil(weather['main']['feels_like'])
    humidity = f"{weather['main']['humidity']}%"
    weather_desc = weather['weather'][0]['description']

    rows = [{
        'Hora': dt_txt,
        'Temperatura': f"{temp}°C",
        'Sensação térmica': f"{feels_like}°C",
        'Humidade': humidity,
        'Descrição do tempo': weather_desc
    }]

    dfWeather = pd.DataFrame(rows)
    print(dfWeather)
else:
    print("Erro: não foi possível obter os dados do clima atual.")

def get_forecast(city, state):
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

forecast = get_forecast(city, state)

if forecast is not None and 'list' in forecast:
    forecast_list = forecast['list']

    today = datetime.now(pytz.timezone('America/Sao_Paulo')).date()
    today_weekday = today.weekday() 

    daily_data = {}

    for entry in forecast_list:

        date = entry['dt_txt'].split(" ")[0]
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        
        weekdays = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM']

        days_difference = (date_obj - today).days
        if days_difference >= 0:
            day_sig = weekdays[(today_weekday + 1 + days_difference) % 7]
        else:
            continue

        temp = round(entry['main']['temp'])
        feels_like = round(entry['main']['feels_like'])
        temp_min = round(entry['main']['temp_min'])
        temp_max = round(entry['main']['temp_max'])
        humidity = entry['main']['humidity']
        weather_desc = entry['weather'][0]['description']
        pop = round(entry.get('pop', 0) * 100)

        if day_sig not in daily_data:
            daily_data[day_sig] = {
                'temps': [],
                'feels_like': [],
                'temp_min': [],
                'temp_max': [],
                'humidity': [],
                'pop': [],
                'descriptions': []
            }
        daily_data[day_sig]['temps'].append(temp)
        daily_data[day_sig]['feels_like'].append(feels_like)
        daily_data[day_sig]['temp_min'].append(temp_min)
        daily_data[day_sig]['temp_max'].append(temp_max)
        daily_data[day_sig]['humidity'].append(humidity)
        daily_data[day_sig]['pop'].append(pop)
        daily_data[day_sig]['descriptions'].append(weather_desc)

    rows = []
    for day_abbr, data in daily_data.items():
        avg_temp = round(sum(data['temps']) / len(data['temps']))
        avg_feels_like = round(sum(data['feels_like']) / len(data['feels_like']))
        avg_humidity = round(sum(data['humidity']) / len(data['humidity']))
        avg_pop = round(sum(data['pop']) / len(data['pop']))

        max_temp = max(data['temp_max'])
        min_temp = min(data['temp_min'])

        most_common_desc = Counter(data['descriptions']).most_common(1)[0][0]

        rows.append({
            'Dia': day_sig,
            'Temperatura média': f"{avg_temp}°C",
            'Sensação térmica média': f"{avg_feels_like}°C",
            'Temperatura mínima': f"{min_temp}°C",
            'Temperatura máxima': f"{max_temp}°C",
            'Humidade média': f"{avg_humidity}%",
            'Chance média de chuva': f"{avg_pop}%",
            'Descrição mais comum': most_common_desc
        })

    dfForecast = pd.DataFrame(rows)
    print(dfForecast)
else:
    print("Erro: não foi possível obter os dados de previsão do tempo.")
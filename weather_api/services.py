# https://www.visualcrossing.com/resources/documentation/weather-api/timeline-weather-api/#request-endpoints
import requests
import os
import pdb

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"


def get_weather(city):
    """Fetch weather data from weather.visualcrossing.com"""
    params = {"location": city, "key": API_KEY}
    response = requests.get(BASE_URL, params=params)
    return response.json()['currentConditions']

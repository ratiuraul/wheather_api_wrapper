"""
Define wheater API routes and View Functions
"""

import json

from flask import Blueprint

from weather_api.services import get_weather

weather_bp = Blueprint('weather', __name__)


@weather_bp.route('/weather/<city>', methods=['GET'])
def city_weather(city: str) -> json:
    """
    Call 3rd party api for given city name.
    :param city: name of the city to get weather data for
    :returns: json object with weather data
    """
    weather_data = get_weather(city)
    return weather_data

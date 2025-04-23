"""
Define wheater API routes and View Functions
"""
import json
from functools import wraps

from flask import Blueprint, jsonify
from requests.exceptions import HTTPError

from weather_api.services import get_forecast, get_weather

weather_bp = Blueprint('weather', __name__)


def handle_client_errors(func):
    """Decorator to handle errors and display usefull messages to clients."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        except HTTPError as http_error:
            return jsonify({
                "status": "error",
                "message": f"External service error: \
{http_error.response.status_code} - {http_error.response.text}"
            }), http_error.response.status_code

    return wrapper


@weather_bp.route('/weather/<city>', methods=['GET'])
@handle_client_errors
def city_weather(city: str) -> json:
    """
    Call 3rd party api for given city name.
    :param city: name of the city to get weather data for
    :returns: json object with weather data
    """
    weather_data = get_weather(city)
    return weather_data.json()


@weather_bp.route('/forecast/<city>', methods=['GET'])
@handle_client_errors
def city_forecast(city: str) -> json:
    """
    Call 3rd paty api to get the 15 days forecast for given city
    :param city: name of the city to get wheather data for
    :returns: json object with weather data
    """
    weather_data = get_forecast(city)
    return weather_data.json()

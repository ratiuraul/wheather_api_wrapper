# https://www.visualcrossing.com/resources/documentation/weather-api/timeline-weather-api/#request-endpoints
import requests
import os
import pdb
from requests.exceptions import HTTPError, Timeout, RequestException, ConnectionError
import logging

error_logger = logging.getLogger("Flask Error Logger")
error_logger.setLevel(logging.ERROR)

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"


def handle_request_errors(func):
    """Decorator to handle request errors."""
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            response.raise_for_status()
            return response
        except HTTPError as http_error:
            error_logger.error(f"HTTP error: {http_error}")
        except ConnectionError as connection_error:
            error_logger.error(f"Connection error: {connection_error}")
        except Timeout as timeout_error:
            error_logger.error(f"Timeout error: {timeout_error}")
        except RequestException as request_error:
            error_logger.error(f"Request error: {request_error}")
        except Exception as e:
            error_logger.error(f"General error: {e}")
    return wrapper


@handle_request_errors
def get_weather(city):
    """Fetch weather data from weather.visualcrossing.com"""
    city_url = BASE_URL + f"/{city}/today"
    params = {
        "include": "current",
        "key": API_KEY,
        "unitGroup": "metric"

    }
    response = requests.get(city_url, params=params)
    return response

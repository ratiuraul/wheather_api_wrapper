"""
Define services that are connecting to 3rd party API.
"""
# https://www.visualcrossing.com/resources/documentation/weather-api/timeline-weather-api/#request-endpoints
import logging
import os
from datetime import datetime

import requests
from requests.exceptions import HTTPError, RequestException, Timeout

from .extensions import cache

error_logger = logging.getLogger("Flask Error Logger")
error_logger.setLevel(logging.ERROR)

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"


def handle_request_errors(func):
    """Decorator to handle request errors."""
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            if isinstance(response, requests.Response):
                # in case response is from cache, it will be a dict
                response.raise_for_status()
                return response.json()
            return response
        except HTTPError as http_error:
            error_logger.error("HTTP error: %s", http_error)
            raise http_error
        except ConnectionError as connection_error:
            error_logger.error("Connection error: %s", connection_error)
            raise connection_error
        except Timeout as timeout_error:
            error_logger.error("Timeout error: %s", timeout_error)
            raise timeout_error
        except RequestException as request_error:
            error_logger.error("Request error: %s", request_error)
            raise request_error
        except Exception as e:
            error_logger.error("General error: %s", e)
            raise e
    return wrapper


@handle_request_errors
def get_weather(city):
    """Fetch weather data from weather.visualcrossing.com"""
    redis_key = f"{city}_{datetime.today().date()}"

    cached_data = cache.get(redis_key)
    if cached_data:
        print("Returning from cache")
        return cached_data

    city_url = BASE_URL + f"/{city}/today"
    params = {
        "include": "current",
        "key": API_KEY,
        "unitGroup": "metric"

    }
    response = requests.get(city_url, params=params, timeout=10)
    # set cache data if no Exception
    # since this is todays weather, it makes sense to cache for 24h
    cache.set(redis_key, response.json(), timeout=86400)

    return response

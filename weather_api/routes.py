from flask import Blueprint, jsonify
from .services import get_weather


weather_bp = Blueprint('weather', __name__)


@weather_bp.route('/weather/<city>', methods=['GET'])
def city_weather(city):
    weather_data = get_weather(city)
    return jsonify(weather_data)

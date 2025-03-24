"""
Module for 3rd party weather API and Redis Cache
"""

from dotenv import load_dotenv
from flask import Flask

from .routes import weather_bp
from .services import error_logger

load_dotenv()

app = Flask(__name__)
app.logger = error_logger
app.register_blueprint(weather_bp, url_prefix='/api')

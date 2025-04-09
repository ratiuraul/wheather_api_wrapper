"""
Module for 3rd party weather API and Redis Cache
"""
from dotenv import load_dotenv
from flask import Flask
from .routes import weather_bp
from .services import error_logger
from .extensions import cache

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.logger = error_logger
    # Initialize the cache extension
    cache.init_app(app)
    # app blueprints
    app.register_blueprint(weather_bp, url_prefix='/api')
    return app

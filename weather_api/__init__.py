from flask import Flask
from dotenv import load_dotenv
from .routes import weather_bp
from .services import error_logger
load_dotenv()

app = Flask(__name__)
app.logger = error_logger
app.register_blueprint(weather_bp, url_prefix='/api')

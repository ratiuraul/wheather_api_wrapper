from flask import Flask
from dotenv import load_dotenv
from .routes import weather_bp
load_dotenv()

app = Flask(__name__)
app.register_blueprint(weather_bp, url_prefix='/api')

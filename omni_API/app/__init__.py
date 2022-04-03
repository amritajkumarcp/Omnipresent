from flask import Flask
from config import ProductionConfig


app = Flask(__name__)

app.config.from_object(ProductionConfig())

import json
from app import views

from flask_caching import Cache  # Import Cache from flask_caching module

cache = Cache(app)  # Initialize Cache
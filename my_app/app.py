from flask import Flask
from flask_cors import CORS
from config import DevelopmentConfig

app = Flask(__name__)
CORS(app)
app.config.from_object(DevelopmentConfig)

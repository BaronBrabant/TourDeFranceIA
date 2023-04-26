from flask import Flask
from flask_session import Session
from flask_cors import CORS
from config import DevelopmentConfig

app = Flask(__name__)
CORS(app)
#app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config.from_object(DevelopmentConfig)

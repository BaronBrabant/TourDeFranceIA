from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user, login_remembered
from .forms import *
from .models import *
from .database import db
import json

tdf_routes = Blueprint('my_blueprint', __name__)

"""
MainPage with the list of all the jokes
"""
@tdf_routes.route('/')
def main():


   # list of the information jokes without the joke itself

    return render_template('playerDialogBox.html')





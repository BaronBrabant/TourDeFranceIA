from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user, login_remembered
from .forms import *
from .models import *
from .database import db
import json
import ast
import os

tdf_routes = Blueprint('my_blueprint', __name__)

"""
MainPage with the list of all the jokes
"""
@tdf_routes.route('/', methods = ['GET', 'POST'])
def main():

 

   if request.method == "POST":

      info = request.get_data()

      print(info)

      """
      f = open("saveRatioFirstLeg.txt", "w")
 
      listRatio = request.form["data"]
      listRatio = json.loads(listRatio)
      print(listRatio)
      f.write(str(listRatio))
      f.close()
      """


   positions = loadRatiosFromFile()

   return render_template('playerDialogBox.html', positions = positions)




def loadRatiosFromFile():
   fil = open("saveRatioFirstLeg.txt", "r")
   positions = fil.read()

   positions = ast.literal_eval(positions)

   return positions




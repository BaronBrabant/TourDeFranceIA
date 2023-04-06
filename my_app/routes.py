from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user, login_remembered
from .forms import *
from .models import *
from .database import db
import json
import ast

tdf_routes = Blueprint('my_blueprint', __name__)

"""
MainPage with the list of all the jokes
"""
@tdf_routes.route('/', methods = ['GET', 'POST'])
def main():

   if request.method == "POST":
      f = open("saveRatio.txt", "w")
 
      listRatio = request.form["data"]
      listRatio = json.loads(listRatio)
      print(listRatio)
      f.write(str(listRatio))
      f.close()

   """
   fil = open("saveRatio.txt", "r")
   positions = fil.read()

   opens = 0
   closes = 0
   for i in positions:
      if i == "[":
         opens += 1
      if i == "]":
         closes += 1

   print(opens)
   print(closes)

   positions.strip()
   print(positions)


   positions = ast.literal_eval(positions)
   print(positions)

   #varTemp = {"data": positions}

   #varTemp = json.loads(varTemp)

   #print(varTemp


   # list of the information jokes without the joke itself
 """
   position = [0.30859375, 0.4482758620689655]
  

   return render_template('playerDialogBox.html', position = position)





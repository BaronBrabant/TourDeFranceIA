from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user, login_remembered
from .forms import *
from .models import *
from .database import db
import ast
from .card import initiate_cards_deck, cards_distribution, cards_distribution_to_a_team, remove_card, lucky_case, exchange_case


tdf_routes = Blueprint('my_blueprint', __name__)



"""
MainPage with the list of all the jokes
"""
@tdf_routes.route('/', methods = ['GET', 'POST'])
def main():

   try:
      if session["gameStarted"] == True:
         pass
   except KeyError: 
      session["gameStarted"] = True
      session["deck"] = []
      session["teams"] = [[] for _ in range(4)]

      session["deck"] = initiate_cards_deck()
      cards_distribution(session["deck"], session["teams"])
      session["gameStarted"] = True
      session["turn"] = -1

   session["turn"]+=1
   session["turn"] = session["turn"]%4
   

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

   return render_template('playerDialogBox.html', positions = positions, teams = session["teams"], teamPlaying = session["turn"])




def loadRatiosFromFile():
   fil = open("saveRatioFirstLeg.txt", "r")
   positions = fil.read()

   positions = ast.literal_eval(positions)

   return positions




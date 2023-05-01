from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
import requests
from flask_login import login_user, logout_user, login_required, current_user, login_remembered
from .forms import *
from .models import *
from .database import db
import ast
import os
from .card import initiate_cards_deck, cards_distribution, cards_distribution_to_a_team, remove_card, lucky_case, exchange_case
import json



tdf_routes = Blueprint('my_blueprint', __name__)



"""
MainPage with the list of all the jokes
"""
@tdf_routes.route('/', methods = ['GET', 'POST'])
def main():

   
   if not os.path.exists("saveGameState.txt"):
      deck = []
      teams = [[] for _ in range(4)]
      deck = initiate_cards_deck()
      cards_distribution(deck, teams)
      gameState = {"deck": deck, "teams": teams, "turn": -1}
      saveGameState(gameState)
      positionEveryone = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
      savePlayerState(positionEveryone)

      

   gameState = loadGameState()
   gameState = gameState.replace("'", '"')
   gameState = json.loads(gameState)


   deck = gameState["deck"]
   teams = gameState["teams"]
   turn = gameState["turn"]
   
   turn = (turn+1)%4
   responseBot = " "

   if request.method == "POST":

      info = request.get_data()
      info = json.loads(info)

      try:
         responseBot = info['testData']['id']
         print(info['testData']['id'])
         print(type(responseBot))
      except KeyError:
         print(info)
         
         info = ast.literal_eval(info["allCyclists"])
         print(info)

         info = sorted(info, key = lambda x: x[4])
         
         positionEveryone = []
         for cyclist in info:
            positionEveryone.append([cyclist[0], cyclist[1]])
         
         savePlayerState(positionEveryone)
      
      return redirect(url_for('my_blueprint.main'))
      """
      f = open("saveRatioFirstLeg.txt", "w")
 
      listRatio = request.form["data"]
      listRatio = json.loads(listRatio)
      print(listRatio)
      f.write(str(listRatio))
      f.close()
      """   


   positions = loadRatiosFromFile()
   positionEveryone = loadPlayerState()
   print(positionEveryone)

   positionEveryone[0][0]

   positionPlayerOnMap = []

   positionCyc =[2, 1]
   print(positions[positionCyc[0]][positionCyc[1]][0])
   print(positions[positionCyc[0]][positionCyc[1]][1])

   for positionCyc in positionEveryone:
      if positionCyc[0] == 0:
         positionPlayerOnMap.append([positions[0][0], 0.48])
      else:
         positionPlayerOnMap.append([positions[positionCyc[0]][positionCyc[1]][0], positions[positionCyc[0]][positionCyc[1]][1]])

   print(positionPlayerOnMap)

   teamCountry = ["Belgium","Germany", "Netherlands", "Italy"]
   print(turn)
   teamPlayingCountry = teamCountry[turn]

   
 

   saveGameState({"deck": deck, "teams": teams, "turn": turn})
   #savePlayerState(positionEveryone)

   return render_template('playerDialogBox.html', positions = positions, teams = teams, teamPlaying = turn, country = teamPlayingCountry, positionEveryone = positionEveryone, positionPlayerOnMap =positionPlayerOnMap)


@tdf_routes.route('/saveRatio', methods = ['GET', 'POST'])
def saveRatio():


   f = open("saveRatioFirstLegV2.txt", "w")

   listRatio = request.form["data"]
   listRatio = json.loads(listRatio)
   print(listRatio)
   f.write(str(listRatio))
   f.close()

   return ('', 204)


@tdf_routes.route('/API/prolog/game', methods = ['GET', 'POST'])
def callProlog():
   info = request.get_data()

   call = requests.post('http://127.0.0.1:3000/API/play', data = info)
   print(info)
   return ('', 204)

@tdf_routes.route('/API/prolog/game/response', methods = ['GET', 'POST'])
def responseProlog():


   info = request.get_data()
   info = json.loads(info)

   print(info)

   info = ast.literal_eval(info["allCyclists"])
   print(info)

   info = sorted(info, key = lambda x: x[4])

   positionEveryone = []
   for cyclist in info:
      positionEveryone.append([cyclist[0], cyclist[1]])

   savePlayerState(positionEveryone)

   return redirect(url_for('/'))

@tdf_routes.route('/API/prolog/chatbot', methods = ['GET', 'POST'])
def callChatbot():

   info = request.get_data()
   info = json.loads(info)
   print(info)
   return jsonify(info)

def loadRatiosFromFile():
   fil = open("saveRatioFirstLegV2.txt", "r")
   positions = fil.read()

   positions = ast.literal_eval(positions)

   return positions

def loadGameState():
   file = open("saveGameState.txt", "r")
   gameState = file.read()

   return gameState

def loadPlayerState():
   fil = open("savePlayerState.txt", "r")
   positions = fil.read()
   positions = ast.literal_eval(positions)

   return positions

def savePlayerState(playerState):
   file = open("savePlayerState.txt", "w")
   file.write(str(playerState))
   file.close()


def saveGameState(gameState):
   file = open("saveGameState.txt", "w")
   file.write(str(gameState))
   file.close()


@tdf_routes.route('/saveRatio', methods = ['GET', 'POST'])
def saveRatio():

  
   f = open("saveRatioFirstLegV2.txt", "w")

   listRatio = request.form["data"]
   listRatio = json.loads(listRatio)
   print(listRatio)
   f.write(str(listRatio))
   f.close()

   return ('', 204)
      
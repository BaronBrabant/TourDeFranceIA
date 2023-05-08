from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
import requests
from flask_login import login_user, logout_user, login_required, current_user, login_remembered
from .forms import *
from .models import *
import ast
import os
from .card import *
import json



tdf_routes = Blueprint('my_blueprint', __name__)



"""
MainPage with the list of all the jokes
"""
@tdf_routes.route('/', defaults={'increaseTurn' : False}, methods = ['GET', 'POST'])
@tdf_routes.route('/<increaseTurn>', methods = ['GET', 'POST'])
def main(increaseTurn = False):

   
   if not os.path.exists("saveGameState.txt"):
      deck = []
      teams = [[] for _ in range(4)]
      deck = initiate_cards_deck()
      cards_distribution(deck, teams)
      gameState = {"deck": deck, "teams": teams, "turn": 0, "sprints":[False, False, False], "points":[]}
      saveGameState(gameState)
      positionEveryone = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
      savePlayerState(positionEveryone)
      saveQuestionAsked(" ")
      call = requests.get('http://127.0.0.1:3000/API/init')

   gameState = loadGameState()
   gameState = gameState.replace("'", '"')
   gameState = ast.literal_eval(gameState)

   

   saveQuestionAskedVar = loadQuestionAsked()
   print(saveQuestionAskedVar)
   print("This is the answer here")

   deck = gameState["deck"]
   teams = gameState["teams"]
   turn = gameState["turn"]
   
   if increaseTurn:
      turn = (turn+1)%4
   responseBot = " "

   """
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
  
      f = open("saveRatioFirstLeg.txt", "w")
 
      listRatio = request.form["data"]
      listRatio = json.loads(listRatio)
      print(listRatio)
      f.write(str(listRatio))
      f.close()
      """   


   positions = loadRatiosFromFile()
   positionEveryone = loadPlayerState()
   #print(positionEveryone)



   positionPlayerOnMap = []
   
   #print(positions)


   for positionCyc in positionEveryone:
      #print(positionCyc)
      if positionCyc[0] == 0:
         positionPlayerOnMap.append([positions[0][0], 0.48])
      else:
         positionPlayerOnMap.append([positions[positionCyc[0]][positionCyc[1]][0], positions[positionCyc[0]][positionCyc[1]][1]])

   print(positionPlayerOnMap)

   teamCountry = ["Belgium","Netherlands", "Germany", "Italy"]
   print(turn)
   teamPlayingCountry = teamCountry[turn]


   saveGameState({"deck": deck, "teams": teams, "turn": turn})

   #savePlayerState(positionEveryone)

   return render_template('playerDialogBox.html', positions = positions, teams = teams, teamPlaying = turn, country = teamPlayingCountry, positionEveryone = positionEveryone, positionPlayerOnMap =positionPlayerOnMap, answerQuestion = saveQuestionAskedVar, responseBot = responseBot)


@tdf_routes.route('/saveRatio', methods = ['GET', 'POST'])
def saveRatio():


   f = open("saveRatioFirstLegV2.txt", "w")

   listRatio = request.form["data"]
   listRatio = json.loads(listRatio)
   print(listRatio)
   f.write(str(listRatio))
   f.close()

   return ('', 204)


@tdf_routes.route('/API/game/', methods = ['GET', 'POST'])
def callProlog():
   info = request.get_data()
   info = json.loads(info)

   #Loading Game State
   gameState = loadGameState()
   gameState = gameState.replace("'", '"')
   gameState = json.loads(gameState)

   deck = gameState["deck"]
   teams = gameState["teams"]
   turn = gameState["turn"] 

   cardPlayed = info['card']
   print(cardPlayed)
   #teamPlaying = info['team']
   #print(teamPlaying)

   print(teams[turn-1])
   
   if turn != 0 and cardPlayed in teams[turn-1]:
      teams[turn-1].remove(cardPlayed)
      print("Card removed from the deck")
      
      call = requests.post('http://127.0.0.1:3000/API/play', json = info)
      print(call)
      
      saveGameState({"deck": deck, "teams": teams, "turn": turn})
   elif turn == 0 and cardPlayed in teams[3]:
      teams[3].remove(cardPlayed)
      print("Card removed from the deck")
      
      call = requests.post('http://127.0.0.1:3000/API/play', json = info)
      print(call)
      
      saveGameState({"deck": deck, "teams": teams, "turn": turn})
   elif turn == 3 and cardPlayed in teams[0]:
      teams[0].remove(cardPlayed)
      print("Card removed from the deck")
      
      call = requests.post('http://127.0.0.1:3000/API/play', json = info)
      print(call)
      
      saveGameState({"deck": deck, "teams": teams, "turn": turn})
      
   else:
      print("Card not in the deck")


   
   
   print("-----------------------")



   #req = requests.get('http://127.0.0.1:3000/API/play')

   
   return ('', 204)

@tdf_routes.route('/API/prolog/game/response', methods = ['GET', 'POST'])
def responseProlog():

   print("this is the call to the response function in flask")
   info = json.loads(request.get_data())
   
   info_cycl = ast.literal_eval(info["allCyclists"])

   info_cycl = sorted(info_cycl, key = lambda x: x[4])
   
   #print(info)

   positionEveryone = []
   for cyclist in info_cycl:
      if cyclist[1] == 0:
         positionEveryone.append([cyclist[0], 0, cyclist[2], cyclist[3]])
      else:
         positionEveryone.append([cyclist[0], cyclist[1]-1, cyclist[2], cyclist[3]])
   
   savePlayerState(positionEveryone)
   
   for cycl in positionEveryone:
      if info["player"] in cycl:
         currentCycl = cycl[:-1]
         fullCycl = cycl

   # Exchanges cards from team deck if player on exchange case
   if currentCycl in exchanges_places:
      # renew cards
      # il faut adapter les fonction dans card.py
      game = ast.eval_literal(loadGameState())
      exchange_case(game["deck"], game["teams"], game["turn"], [game["teams"][game["turn"]][0], game["teams"][game["turn"]][1], game["teams"][game["turn"]][2]])
   
   # Chance case
   if currentCycl in chance_places:
      return jsonify({"card":lucky_case(), "player":fullCycl}), 201
   

   return ('', 200)
   #return redirect(url_for('my_blueprint.main'))

@tdf_routes.route('/API/prolog/chatbot', methods = ['GET', 'POST'])
def callChatbot():

   info = request.get_data()
   info = json.loads(info)
   print(info)

   responseBot = info['testData']['id']

   saveQuestionAsked(responseBot)

   return ('', 200)


@tdf_routes.route('/checkDataChange', methods = ['GET', 'POST'])
def checkDataChange():

   #print("this is polled")

   #this checks if the game data (aka the position of the cyclist have changed)
   if os.path.exists("savePlayerState.txt"):
      if not os.path.exists("savePLayerStateLastVersion.txt"):
         file1 = open("savePlayerState.txt", "r")
         file2 = open("savePLayerStateLastVersion.txt", "w")

         file2.write(file1.read())
         file1.close()
         file2.close()
      else:
         file1 = open("savePlayerState.txt", "r")
         file2 = open("savePLayerStateLastVersion.txt", "r")

         positionCurrent = file1.read()
         positionLastVersion = file2.read()

         positionCurrentDic = ast.literal_eval(positionCurrent)
         positionLastVersionDic = ast.literal_eval(positionLastVersion)

         file1.close()
         file2.close()
         
         print(positionCurrentDic)
         print(positionLastVersionDic)
         

         if positionCurrentDic != positionLastVersionDic:
            print("this was changed here")
            
            #check if player passed a checkpoint
            #checkPlayerPassSprint(positionCurrentDic)
            
            fileToChange = open("savePLayerStateLastVersion.txt", "w")

            fileToChange.write(positionCurrent)
            fileToChange.close()

            return redirect(url_for('my_blueprint.main', increaseTurn = True))

   #this checks if questions asked to the bot have changed
   if os.path.exists("saveQuestionAsked.txt"):
      if not os.path.exists("saveQuestionAskedLastVersion.txt"):
         file1 = open("saveQuestionAsked.txt", "r")
         file2 = open("saveQuestionAskedLastVersion.txt", "w")

         file2.write(file1.read())
         file1.close()
         file2.close()
      else:
         file1 = open("saveQuestionAsked.txt", "r")
         file2 = open("saveQuestionAskedLastVersion.txt", "r")

         currentQuestion = file1.read()
         lastQuestion = file2.read()

         file1.close()
         file2.close()
         

         if currentQuestion != lastQuestion:
            print("this was changed here")
            
            fileToChange = open("saveQuestionAskedLastVersion.txt", "w")

            fileToChange.write(currentQuestion)
            fileToChange.close()

            return redirect(url_for('my_blueprint.main'))

      
   return jsonify("false")
   

def loadRatiosFromFile():
   
   allRatios = []

   for i in range(13):

      file = open("./ratios/saveRatio"+str(i)+".txt", "r")
      positions = file.read()
      positions = ast.literal_eval(positions)

      if (i != 0):
         allRatios.extend(positions[1:])
      else:
         allRatios.extend(positions)
      #print(positions)

   print(allRatios)

   return allRatios

def loadGameState():
   file = open("saveGameState.txt", "r")
   gameState = file.read()
   
   file.close()

   return gameState

def loadPlayerState():
   fil = open("savePlayerState.txt", "r")
   positions = fil.read()
   fil.close()
   positions = ast.literal_eval(positions)

   return positions

def loadQuestionAsked():
   file = open("saveQuestionAsked.txt", "r")
   questionAsked = file.read()
   file.close()
   
   return questionAsked

def savePlayerState(playerState):
   file = open("savePlayerState.txt", "w")
   file.write(str(playerState))
   file.close()


def saveGameState(gameState):
   file = open("saveGameState.txt", "w")
   file.write(str(gameState))
   file.close()

def saveQuestionAsked(questionAsked):
   file = open("saveQuestionAsked.txt", "w")
   file.write(str(questionAsked))
   file.close()





def checkPlayerPassSprint(playerPos):

   gameData = loadGameState() 
   
   sprintState = gameData["sprintState"]
   
   ##the 3 first entries will be the winners of the sprints, the rest is the order by which the player finish and their final position
   pointState = gameData["points"]
   
   if not sprintState[0]:
      #checks if a player went  by the sprint1
      
      for playerState in playerPos:
         
         if playerState[0] >= 22:
            pointState.append(playerState)
            sprintState[0] = True
            gameData["sprintState"] = sprintState
            gameData["points"] = pointState
            saveGameState(gameData)
            return True
            
   if not sprintState[1]:
      
      for playerState in playerPos:
         
         if playerState[0] >= 36:
            pointState.append(playerState)
            sprintState[1] = True
            gameData["sprintState"] = sprintState
            gameData["points"] = pointState
            saveGameState(gameData)
            return True
         
   if not sprintState[2]:
      
      for playerState in playerPos:
         
         if playerState[0] >= 76:
            pointState.append(playerState)
            sprintState[2] = True
            gameData["sprintState"] = sprintState
            gameData["points"] = pointState
            saveGameState(gameData)
            return True
   
   for playerState in playerPos:
      
      res1 = any(playerState[3] in sublist for sublist in pointState)
      
      if playerState[0] >= 95 and not res1:
         pointState.append(playerState)
         gameData["points"] = pointState
         saveGameState(gameData)
         return True
      

def calculateFinalScore():
   
   totalPoints = {}
   
   finalPoints = loadGameState()["points"]
   

      
            
from my_app import app
import os 
#from os.path import exists
import sys 

#app.run(debug=True)

if __name__ == '__main__':

    database_exists = os.path.exists(os.path.dirname(__file__)+ "/saveGameState.txt")

    ## Create the dummy database !!! THIS DELTES ALL DATA IN THE DATABASE !!!   
    if len(sys.argv) > 1:
        if sys.argv[1] == "-create":
            
            if database_exists:
                os.remove(os.path.dirname(__file__)+ "/saveGameState.txt")
                os.remove(os.path.dirname(__file__)+ "/savePlayerState.txt")
                os.remove(os.path.dirname(__file__)+ "/savePlayerStateLastVersion.txt")
                print("Removing existing database.")
    else:
        print("Loading existing database...")

        
    app.run(debug=True)
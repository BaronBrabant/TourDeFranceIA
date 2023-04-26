# Description of the project

This is a tour the france boardgame programmed with the help of tau-prolog in order to implement a player and an AI
This is a first draft of the project meaning the prolog has been implemented and can be called once to move the players.
The website is still a bit shabby meaning you'll need to realod the website to observe the changes in the cyslists
and the response of the chat bot can be observed within the python flask terminal.

The front-end is managed by the flask servers, whilst the backend logic (meaning tau-prolog) runs
on a nodejs server. These two communicate with each other in order to execute the commands.
If a command doesnt work you might have to check if the nodejs server hasnt crashed and if its the case you simply need to reload it.

## Instructions to run it

• Open two terminals in the folder of the project
• In the first terminal in the /TourDeFranceIA path start by executing the pip install -r requirements.txt to download all necessary modules
• Once this is done you can launch the flask server with: python run.py
• Once this is done you can launch the nodejs server by navigating to the /TourDeFranceIA/my_app/static/js path
• Once there run the following command: node app.js
• And you're all set, now the two servers are ready to communicate and you can enter a card you'd like to play by simply entering the integer in the text box
• There are no checks on the cards played yet so be honest!

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

    jokeBought = None
    user_role = False
    isLoggedIn = login_remembered()
    if isLoggedIn == True:  
        user_role = current_user.role

        jokes = db.session.query(association_user_joke.c.joke_id).filter(association_user_joke.c.user_id == current_user.id).all()
        jokeBought = []
        for i in range(len(jokes)):
            jokeBought.append(jokes[i][0])

    jokes = Joke.query.all()
    # list of the information jokes without the joke itself
    jokesDict = []
    for joke in jokes:
        jokesDict.append(joke.littleDict())

    return render_template('home.html', jokes = jokesDict, jokesOwned = jokeBought , isLogged = isLoggedIn, user_role = user_role)


"""
showUsers is used by the admin to show all users signed up on the website and in order to see how many jokes each user bought.
"""
@tdf_routes.route("/showUsers")
@login_required
def showUsers():
    if current_user.role == True:
        list_usernames = []
        list_users = db.session.query(User.id).all()
        users_joke = db.session.query(association_user_joke).all()
        nb_jokes_users = []
        for id in list_users:
            username = db.session.query(User.username).filter(User.id == id[0]).first()
            list_usernames.append(username[0])
            nb_jokes = 0
            for info in users_joke:
                if info[0] == id[0]:
                    nb_jokes += 1
            nb_jokes_users.append(nb_jokes)
        
        
        return render_template("showUsers.html", nb_jokes_users = nb_jokes_users, list_usernames= list_usernames, isLogged = True, user_role = current_user.role)
    else:
        return redirect(url_for('my_blueprint.main'))


from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user, login_remembered
from .forms import *
from .models import *
from .database import db
import json

users_routes = Blueprint('my_blueprint', __name__)

"""
MainPage with the list of all the jokes
"""
@users_routes.route('/')
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
Login
"""
@users_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', form=form, user=current_user, error=None)
    if not form.validate_on_submit():
        return render_template('login.html', form=form, user=current_user, error=None)
    
    user = User.query.filter_by(username=form.username.data).first()
    if user is None:
        return render_template('login.html', form=form, user=current_user, error='This user does not exist.')
    
    login_user(user, remember=True, force=True)
    return redirect("/", code = 302)
    

"""
register page use to create a new user, log him and redirect him to the homepage
"""
@users_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if request.method == 'GET':
        return render_template('register.html', form=form, user=current_user)
    if not form.validate_on_submit():
        return render_template('register.html', form=form, user=current_user)
    
    new_user = createUser(form.username.data, form.name.data, form.surname.data, form.passwd.data, form.email.data)
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user, remember=True, force=True)

    return redirect("/", code = 302)

"""
myProfile pages allows the user to modify its password 
"""
@users_routes.route('/myProfile', methods=['GET', 'POST'])
@login_required
def myProfile():

    user_role = current_user.role

    form = PasswordchangeForm()

    my_data = User.query.filter_by(id=current_user.get_id()).all()

    if request.method == 'GET':
        return render_template('myProfile.html', my_data_list = my_data, form=form, user=current_user, user_role = user_role, isLogged = True)
    if not form.validate_on_submit():
        return render_template('myProfile.html', my_data_list = my_data, form=form, user=current_user, user_role = user_role, isLogged = True)


    user = current_user

    if user.check_password(form.passwd.data):

        user.set_password(form.new_passwd.data)
        db.session.commit()

        return redirect("/", code = 302)

    return render_template('myProfile.html', my_data_list = my_data, form=form, user=current_user, error=None, user_role = user_role, isLogged = True)
    

"""
Logout
"""
@users_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('my_blueprint.main'))

"""
myJokes is the screen that shows all the jokes bought by a user. 
"""
@users_routes.route('/myJokes')
@login_required
def show_jokes():

    jokes = db.session.query(association_user_joke.c.joke_id).filter(association_user_joke.c.user_id == current_user.id).all()
    jokeBought = []
    for i in range(len(jokes)):
        jokeBought.append(jokes[i][0])
    
    jokeBought = tuple(jokeBought)

    jokes = Joke.query.filter(Joke.id.in_(jokeBought)).all()
    jokesDict = []
    for joke in jokes:
        jokesDict.append(joke.littleDict())

    
    user_role = current_user.role

    return render_template("myJokes.html", jokes = jokesDict, isLogged = True, user_role = user_role)

"""
showUsers is used by the admin to show all users signed up on the website and in order to see how many jokes each user bought.
"""
@users_routes.route("/showUsers")
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

"""
The detail route serves to expand a joke when it is clicked on and give the user either more details such as the reviews if not bought or to give access
to the joke if it is already owned. The id number is the id of the joke in the database which is used by Alchemy to track down the joke.
"""            
@users_routes.route("/details/<id>", methods=['GET', 'POST'])
def showJoke(id):

    jokeSql = Joke.query.filter(Joke.id == id).first()
    
    if jokeSql == None:
        return render_template('error.html', status = 403, message='This joke doesnt exist')

    jokeConverted = jokeSql.littleDict()

    review = ReviewForm()
    isLoggedIn = login_remembered()
    joke_info = db.session.query(Joke).filter(Joke.id == id).first()
    

    allReviews = db.session.query(association_user_joke).filter(association_user_joke.c.joke_id == id, association_user_joke.c.review != None).all()

    if isLoggedIn:
        user_role = current_user.role
        assosTableRow = db.session.query(association_user_joke).filter(association_user_joke.c.user_id == current_user.id, association_user_joke.c.joke_id == id).first()
    
        if assosTableRow == None:
            bought = False
        else:
            bought = True
    else:
        bought = False
        user_role = False
    
    usernameList = []
    totalAverage = 0
    for i in range(len(allReviews)):
        
        totalAverage += allReviews[i][3]

        info = (db.session.query(User).filter(User.id == allReviews[i][0]).first())
        usernameList.append(info.username)

    if len(allReviews) == 0:
        totalAverage = 0
    else:
        totalAverage = totalAverage/(len(allReviews))


    if request.method == 'POST':
        if review.comment.data != "" and review.review.data != None:
            updateReview(review.comment.data, review.review.data, id, current_user.id)
            db.session.commit()
    elif request.method == 'GET':
        allReviews = db.session.query(association_user_joke).filter(association_user_joke.c.joke_id == id, association_user_joke.c.review != None).all()
        return render_template('details.html',jokeObj = jokeConverted, form=review, joke = joke_info, isLogged = isLoggedIn, bought = bought, reviewList = allReviews, usernameList = usernameList, score = totalAverage,  user_role = user_role)

    allReviews = db.session.query(association_user_joke).filter(association_user_joke.c.joke_id == id, association_user_joke.c.review != None).all()
    #print(allReviews)

    if not review.validate_on_submit():
        return render_template('details.html', jokeObj = jokeConverted, form=review, joke = joke_info, isLogged = isLoggedIn, bought = bought, reviewList = allReviews, usernameList = usernameList, score = totalAverage,  user_role = user_role)
    
    
    #print(allReviews)
    return redirect(url_for('my_blueprint.showJoke', id = id))
   

"""
The basket route serves to view and access all jokes added to basket in order to review and potentially remove them if unwanted.
Furthermore the route is used to checkout and pay which will then add the jokes bought to the users list through an ajax call.
"""
@users_routes.route('/basket', methods=['get', 'post'])
def basket():
    user_role = False
    isLoggedIn = login_remembered()

    if request.method == "POST":
        listToAdd=request.form['data']
        assert listToAdd != None

        listToAdd = json.loads(listToAdd)

        for indexJoke in listToAdd:
            jokeObj = db.session.query(Joke).filter(Joke.id == indexJoke).first()
            assert jokeObj != None

            jokeObj.user.append(current_user)

        db.session.commit()
    


    if isLoggedIn == True:
        user_role = current_user.role

    return render_template('basket.html', isLogged = isLoggedIn, user_role = user_role)


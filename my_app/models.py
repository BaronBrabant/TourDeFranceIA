from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db

"""
This many-to-many association serves both as the connection between the user and the jokes he bought 
but also as the review table as reviews can only be left by users that own the joke.
"""
association_user_joke = db.Table(
    "association_user_joke",
    db.metadata,
    db.Column("user_id", db.ForeignKey("user.id"), primary_key=True),
    db.Column("joke_id", db.ForeignKey("joke.id"), primary_key=True),
    db.Column('comment', db.String(280), default = "", nullable = False),
    db.Column('review', db.Integer, nullable = True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(1024), unique=True, nullable=False)
    passwd_hash = db.Column(db.String(128))
    role = db.Column(db.Boolean, nullable=False)
    jokes = db.relationship('Joke', secondary = association_user_joke, back_populates = "user")
    
    def set_password(self, passwd):
        self.passwd_hash = generate_password_hash(passwd)
    
    def check_password(self, passwd):
        return check_password_hash(self.passwd_hash, passwd)
    
    def __repr__(self):
        return f'User(username={self.username}, email={self.email})'



class Joke(db.Model):
    __tablename__ = 'joke'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tier = db.Column(db.Integer, nullable = False)
    type = db.Column(db.String(30), nullable = "meh")
    keywords = db.Column(db.String(128), nullable = False)
    description = db.Column(db.String(1024), nullable = False)
    joke = db.Column(db.String(1024), nullable = False)
    author = db.Column(db.String(30), nullable = False)
    price = db.Column(db.Float, nullable = False)
    user = db.relationship("User", secondary = association_user_joke, back_populates = "jokes")
    # reviews = db.relationship('Review', backref='user', lazy='dynamic')
        
    #def __repr__(self):
    #    return f'Message(text={self.text})'
    def littleDict(self):
        thisdict = {
            "id": self.id,
            "tier": self.tier,
            "type": self.type,
            "keywords": self.keywords,
            "author": self.author,
            "price" : self.price
        }
        return thisdict

"""
Function used throughout the routes.py in order to generate a new user.
Takes in parameters collected by the form and generates a user entry which is then returned to 
routes.py to be commited.
"""
def createUser(username, name, firstname, password, email, role = False):
# date pas sûre
    user1 = User(username=username, name=name, surname=firstname,
            role= role, email=email)

    user1.set_password(password)

    return user1

"""
Creates sample data to be pushed when the app is launched in order to be able to interact with the website
"""
def createDummyData():

    user1 = User(
                 username='admin123', 
                 name='henri', 
                 surname='henri',
                 email = 'henri@henri.com',
                 passwd_hash=generate_password_hash('admin123##!wqeq'), 
                 role=True
                )

    user2 = User(
                 username='lambdauser', 
                 name='not henri', 
                 surname='nobody',
                 email = 'lamda@user.com',
                 passwd_hash=generate_password_hash('badpassword123'), 
                 role=False
                )

    jokesToAdd = []

    joke1 = addJokes(2, "dirty", "gynecologist deaf job", "what does a deaf gynecologist do?", "What does a deaf gynecologist do? He reads lips", "Stolen from the internet", 20)
    
    joke2 = addJokes(1, "knock knock", 'KGB questioning', 'What happens when the kgb comes knocking', '#1 Knock Knock #2 who\'s there? #1 slaps person n2, we will ask the questions', 'Inspired from the office', 15)

    joke3 = addJokes(0, "dirty", "prison surprise", "Unexpected sex - thats a great way to...", "Unexpected sex - thats a great way to wake up. If you're not in a prison", "top-funny-jokes.com", 4.99)

    joke4 = addJokes(1, "blondes", "building seeing", "Three blondes walk into a building.", "Three blondes walk into a building. You'd think one of them would've seen it.", "top-funny-jokes.com", 8.50)
    
    joke5 = addJokes(2, "blonde", "blonde 911 police", "why don't blondes call 911...", "Why dont blondes call 911 in an emergency? They can't remeber the number.", "top-funny-jokes.com", 10.99)

    joke6 = addJokes(0, "dirty","dirty frogs", "What did one lesbian frog say to the other?", "What did one lesbian frog say to the other? You know, we do taste like chicken!", "top-funny-jokes.com", 12)

    joke7 = addJokes(0, "dad", "sushi dad-joke", "I would avoid the sushi...", "I would avoid the sushi if I was you. Its a little fishy", "top-funy-jokes.com", 6.99)

    joke8 = addJokes(0, "pun", "rulers stationary", "I like jokes about stationery, but...", "I like jokes about stationery, but rulers are where I draw the line.", "scienceofpeople.com", 2.99)

    joke9 = addJokes(0, "flat earth", "70% water flat", "70%/ of the earth is water, ...", "70%/ of the earth is water, and virutally none of it is carbonated. So the earth is, in fact, flat.", "scienceofpeople.com", 1.99)

    joke10 = addJokes(2, "plagiarism", "plagiarism nothing", "logic of plagiarism", "Plagiasim: Getting in trouble for something you didn't do.", "scienceofpeople.com", 21)

    joke11 = addJokes(0, "dirty", "differece snowman snowwoman", "Whats the difference between a snowman and snowwoman?", "Whats the difference between a snowman and a snowwoman? The snow balls", "Benjamin heard it as a child", 1.99)

    joke12 = addJokes(0, "children", "kangoroo jump house", "Can a kangoroo jump higher than a house?", "Can a kangoroo jump higher than a house? Of course not a house can't jump.", "Young Benjamin", 3.99)

    #add jokes to already bought list to simulate other clients
    joke1.user.append(user1)
    joke2.user.append(user1)
    joke5.user.append(user1)
    joke6.user.append(user1)

    joke1.user.append(user2)
    joke2.user.append(user2)
    joke4.user.append(user2)
    joke6.user.append(user2)



    db.session.add(joke1)
    db.session.add(joke2)

    #adds all jokes defined above except for 1 and 2 as they are added to purchase list of simulated clients
    jokesToAdd.extend([joke3, joke4, joke5, joke6, joke7, joke8, joke9, joke10, joke11, joke12])

    commitJokes(jokesToAdd)

    updateReview("amazing joke lol", 4, 1, 1)
    updateReview("lmao cant take it", 5, 2, 1)
    updateReview("rofl", 4, 5, 1)
    updateReview("amazing", 4, 6, 1)

    updateReview("lol", 3, 1, 2)
    updateReview("jokes", 4, 2, 2)
    updateReview("lol", 3, 4, 2)
    updateReview("amazing", 4, 6, 2)
    

    db.session.commit()

    #This is how you can check what jokes were sold in general aka if user1 and user 2 buy joke 1 and only user 1 buys joke 2 the return will be [<Joke 1>, <Joke 2>]
    #print("this is the database association table")
    #jokes = Joke.query.join(User, Joke.user).all()
    #print(jokes)

    #querying the whole association table will return a list of tuples with the information of who bought what exactly with their review and comments so the return will be:
    #[(1, 2, "Hello is it me you're looking for", None), (1, 1, "Hello is it me you're looking for", None), (2, 1, "Hello is it me you're looking for", None)]
    #varTest = db.session.query(association_user_joke).all()
    #print(varTest)


   

"""
Used to simplify the creation of dummy data (or more precicely of the jokes) for the sake of testing
"""
def addJokes(tier, type, keywords, description, joke, author, price):

    jokeReturn = Joke(
            tier = tier, # where 2 is platinum and 0 is dirt
            type = type, 
            keywords = keywords,
            description = description,
            joke = joke,
            author = author,
            price = price
        )

    assert jokeReturn != None

    return jokeReturn

"""
Used by routes.py to updates reviews in the database meaning adding a review comment and score to the association table representing
both the ownership of a joke by a user and the review he left on the joke.
This was done as a user can only review jokes he ownes.
"""
def updateReview(comment, review, jokeId, userId):

    upd = db.update(association_user_joke)
    #say what the new value needs to be
    val = upd.values({"review":review})
    val0 = upd.values({"comment":comment})
    #set the conditions aka which row you want to update in our case
    cond = val.where(association_user_joke.c.user_id == userId, association_user_joke.c.joke_id == jokeId)
    cond0 = val0.where(association_user_joke.c.user_id == userId, association_user_joke.c.joke_id == jokeId)
    #execute the update
    db.session.execute(cond)
    db.session.execute(cond0)

def commitJokes(listJokes):
    for joke in listJokes:
        db.session.add(joke)

    db.session.commit()



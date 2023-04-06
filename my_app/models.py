from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(1024), unique=True, nullable=False)
    passwd_hash = db.Column(db.String(128))
    role = db.Column(db.Boolean, nullable=False)
    
    def set_password(self, passwd):
        self.passwd_hash = generate_password_hash(passwd)
    
    def check_password(self, passwd):
        return check_password_hash(self.passwd_hash, passwd)
    
    def __repr__(self):
        return f'User(username={self.username}, email={self.email})'


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

   

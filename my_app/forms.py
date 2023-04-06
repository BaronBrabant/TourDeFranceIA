from sqlite3 import Date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, IntegerField
from wtforms.validators import Length, InputRequired, ValidationError, Email, DataRequired
from .models import User
from werkzeug.security import check_password_hash
from .database import db
from flask_login import current_user


name_validators = [InputRequired(), Length(min=3, max=30)]
email_validators = [InputRequired(), Email()]
passwd_validators = [InputRequired(), Length(min=6, message='Password should be at least %(min)d characters long')]


class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=name_validators)
    name = StringField(label='name', validators=name_validators)
    surname = StringField(label='surname', validators=name_validators)
    email = EmailField(label='Email', validators=email_validators)
    passwd = PasswordField(label='Password', validators=passwd_validators)
    passwd_confirm = PasswordField(label='Confirm password')
    submit = SubmitField(label='Register')
    
    def validate_passwd_confirm(self, passwd_confirm):
        if passwd_confirm.data != self.passwd.data:
            raise ValidationError('Wrong password confirmation.')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This user already exist. Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email address is already registered.')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[InputRequired()])
    passwd = PasswordField(label='Password', validators=[InputRequired()])
    submit = SubmitField(label='Log-in')

    def validate_passwd(self, passwd):
        hashed = db.session.query(User.passwd_hash).filter_by(username=self.username.data).first()

        if not check_password_hash(hashed[0], passwd.data):
            raise ValidationError('Wrong password.')

class ReviewForm(FlaskForm):
    comment = StringField(label='Comment', validators=[DataRequired()])
    review = IntegerField(label = 'Star review' , validators=[DataRequired()])
    submit = SubmitField(label='Submit')
    
class PasswordchangeForm(FlaskForm):
    passwd = PasswordField(label='Password', validators=[InputRequired()])
    new_passwd = PasswordField(label='New password', validators=passwd_validators)
    new_passwd_confirm = PasswordField(label='Confirm password')
    submit = SubmitField(label='Change password')

    def validate_passwd(self, passwd):
        hashed = db.session.query(User.passwd_hgitash).filter_by(username=current_user.username).first()
        
        if not check_password_hash(hashed[0], passwd.data):
            raise ValidationError('Wrong password.')
    

    def validate_new_passwd_confirm(self, new_passwd_confirm):
        if new_passwd_confirm.data != self.new_passwd.data:
            raise ValidationError('Wrong password confirmation.')
from .app import app
from .login_manager import login_manager
from .database import db
from .routes import users_routes
from .models import *

app.register_blueprint(users_routes)


with app.app_context():
    db.drop_all()
    db.create_all()

    createDummyData()

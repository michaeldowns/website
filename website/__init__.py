from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.mail import Mail

# Initialize app
app = Flask(__name__)

# Load config
app.config.from_object('config.DevelopmentConfig')

# Load extensions
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view =  "login.page"

# Register blueprints
from .views import blueprints
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# Extension config
from .models import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


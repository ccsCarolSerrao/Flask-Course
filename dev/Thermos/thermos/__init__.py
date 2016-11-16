import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.moment import Moment

basedir = os.path.abspath(os.path.dirname(__file__))

#Configure DataBase
app = Flask(__name__)
app.config['SECRET_KEY'] = '\xe6\xb5\x95Z\xbb\xe9\x05\xf2%\x87T\xbf5\xc3\xfb!\x94\xaf\x7f\xdc\x8b\x9e\xa1\x19'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)

#Configure Authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.init_app(app)

#For displaying timestamp
moment = Moment(app)

from thermos import models, views
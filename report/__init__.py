
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import mongoengine as db



app = Flask(__name__)
db.connect(host=DB_URI)
app = Flask(__name__)

CSRFProtect(app)

app.secret_key  = "key_whatever"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["WTF_CSRF_ENABLED"] = True

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from report import routes
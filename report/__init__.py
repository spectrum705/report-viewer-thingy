
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import mongoengine as db
from pymongo import MongoClient

from dotenv import load_dotenv
load_dotenv()

DB_URI = os.getenv('DB_URI')  or os.environ["DB_URI"]

# if "DB_URI" in os.environ:
#     DB_URI = os.environ['DB_URI']
# else:
#     from report.config import DB_URI


app = Flask(__name__)




db.connect(host=DB_URI)
pymongo_client = MongoClient(DB_URI)
app = Flask(__name__)

CSRFProtect(app)

app.secret_key  = "key_whatever"
app.config["WTF_CSRF_ENABLED"] = True

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from report import routes
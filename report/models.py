
from flask_login import UserMixin
from report import db, login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    #this is our database model of a user, made more changes will upload later

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    username = db.Column(db.String(20), nullable = False)
    password = db.Column(db.String(20), nullable=False)
    userType = db.Column(db.String(10), nullable=False)
    theClass = db.Column(db.String())
    fileName = db.Column(db.String())
    fileData = db.Column(db.LargeBinary)

    
    def __repr__(self):
        return f"User('{self.username}','{self.id}',{self.userType}, {self.theClass}, {self.fileName})"




from re import sub
from flask_login import UserMixin
from report import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return Teachers.objects(_id=int(user_id)).first()
    #this is our database model of a user, made more changes will upload later


class Teachers(db.DynamicDocument, UserMixin):
    _id=db.IntField(primary_key=True)
    name=db.StringField(max_length=20, required=True)
    # password = db.StringField( required=True)
    classes=db.ListField(db.DictField())
    isAdmin=db.BooleanField()
    isStudent=db.BooleanField()
        
  
    def to_json(self):
        return {
            "name":self.name,
            "password":self.password,
            "id":self._id,
            "classes": self.classes
        }
    
   

class Marks(db.DynamicEmbeddedDocument):
    pass
    # test_1=db.DictField()
    # test_2=db.DictField()
    # test_3=db.DictField()
    # test_4=db.DictField()

class Students(db.Document):
    _id=db.IntField(primary_key=True) #enter admission no here
    name=db.StringField( required=True)
    standard = db.StringField(required=True)
    marks=db.EmbeddedDocumentField(Marks)
    isGraded=db.BooleanField
    # roll_number=db.IntField(required=True)
    
class Attendance(db.DynamicDocument):
    _id=db.IntField(primary_key=True)
    name=db.StringField(max_length=20, required=True)
    school=db.StringField(max_length=20, required=True)
    semester=db.IntField(required=True)

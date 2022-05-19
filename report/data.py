import random 
from mongoengine import *
import os

# DB_URI = os.environ['DB_URI']
connect(host=DB_URI)



teacher_dummy_data={
    "teacher_1":{
                "teacher_id": 1,
                "password":"pass#teacher_1",
                "classes":["class_1-english",                              
                         ]      
                },
    
    "teacher_2":{
                "teacher_id": 2,
                "password":"pass#teacher_2",
                 "classes":["class_1-english", 
                            "class_2-science",              
                         ]                     
                }  
}
    # mongoengine data model 
    

class Teachers(Document):
    _id=IntField(primary_key=True)
    name=StringField(max_length=20, required=True)
    password = StringField(max_length=20, required=True)
    classes=ListField(DictField())
        
# teacher_dummy_data={
#               { "name":#"teacher_1"
#                   "teacher_id": 1,
#                 "password":"pass#teacher_1",
#                 "classes":["class_1-english",                              
#                          ]      
#                 },
# }


# find a way to make a variable attriute in teacher_list
teacher=Teachers(name="teacher_1",_id=random.randint(1,100000),password="pass#teacher_1",classes=[{"class_1":"english"}, {"class_2":"science"}])
teacher.save()
    
user= Teachers.objects(name="teacher_1")    

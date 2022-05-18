from mongoengine import *



# DB_URI = add URI here
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
    
class Classes(EmbeddedDocument):
    classes=ListField(StringField(max_length=20))

class Teacher(EmbeddedDocument):
    
    teacher_id=IntField(primary_key=True)
    password = StringField(max_length=20, required=True)
    classes=EmbeddedDocumentField(Classes)
    
class TeacherList(Document):
   EmbeddedDocumentField(Teacher)
    


             
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

classes=Classes(classes=["class_1-english", "class_2-science"])
teacher=Teacher(teacher_id=1, password="pass#teacher_1", classes=classes)
teacher_list=TeacherList(name=teacher)
teacher_list.save()
    
    
    
    
teacher_list.save()
    
    
    

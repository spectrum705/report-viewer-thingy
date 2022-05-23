import random 
from mongoengine import *
import os
# from report import db
import csv,os
from pathlib import Path
from report.models import Teachers, Students, Marks
  

# DB_URI = os.environ['DB_URI']

# connect(host=DB_URI)
# mongoengine data model 
connect(host=DB_URI)

# class Teachers(Document):
#     _id=IntField(primary_key=True)
#     name=StringField(max_length=20, required=True)
#     password = StringField(max_length=20, required=True)
#     classes=ListField(DictField())
#     isAdmin=BooleanField()


    


student_dummy_data = {
   "class_1":{ "students": [
               
                    {"admission_no": 1, "name": "tewo", "marks": {
                                                    "test_1":{"maths": None, "english": None, "science": None},
                                                    "test_2":{"maths": None, "english": None, "science": None},
                                                    "test_3":{"maths": None, "english": None, "science": None},
                                                    "test_4":{"maths": None, "english": None, "science": None}
                                                    }
                    },
                    
                    {"admission_no": 2, "name": "naruto", "marks": {
                                                    "test_1":{"maths": None, "english": None, "science": None},
                                                    "test_2":{"maths": None, "english": None, "science": None},
                                                    "test_3":{"maths": None, "english": None, "science": None},
                                                    "test_4":{"maths": None, "english": None, "science": None}
                                                    }
                    },
         ]
   },}

# class Marks(EmbeddedDocument):
#     test_1=DictField()
#     test_2=DictField()
#     test_3=DictField()
#     test_4=DictField()

# class Students(Document):
#     _id=StringField(primary_key=True) #enter admission no here
#     name=StringField( required=True)
#     standard = StringField(required=True)
#     marks=EmbeddedDocumentField(Marks)
    

# marks=Marks(test_1={"maths": None, "english": None, "science": null},)
# student=Students(name="tewo",_id=random.randint(1,100000),standard="class_1",marks=marks)
# student.save()

# making a subject list for all classes




# csv file name
def createDb():
    # learn about relative path and absolute path
    folder = Path("report/school_data")
    data_file = folder/"student_dummy_data.csv"
    # data_file = r"C:\Users\SHUBHAM\Desktop\report-viewer-thingy\report\school_data\student_dummy_data.csv"
    with open(data_file, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        #username theClass userType
        #student1   7      student
        for row in csvreader:
            if row[0].lower() != 'admission number':
                # enc_password = bcrypt.generate_password_hash( "pass#"+row[0].lower()).decode('utf-8')
                # usr = User(username = row[0].lower(), userType = row[2].lower()
                student = Students(_id= str(row[0]), name=row[1], standard=row[2] ,marks=Marks(test_1={"maths": None, "english": None, "science": None, "social studies":None, "hindi":None}, test_2={"maths": None, "english": None, "science": None, "social studies":None, "hindi":None}, test_3={"maths": None, "english": None, "science": None, "social studies":None, "hindi":None}, test_4={"maths": None, "english": None, "science": None, "social studies":None, "hindi":None}))
                student.save()
                
                print(f"name: {row[1]}, class: {row[2]}, added")
    # os.remove(data_file)
    return True



createDb()
teacher=Teachers(name="teacher_1",_id=random.randint(1,100000),password="pass#teacher_1",classes=[{"class_9":"english"}])
teacher.save()

teacher=Teachers(name="teacher_2",_id=random.randint(1,100000),password="pass#teacher_2",classes=[{"class_9":"maths"}])
teacher.save()

teacher=Teachers(name="teacher_3",_id=random.randint(1,100000),password="pass#teacher_3",classes=[{"class_9":"social studies"}])
teacher.save()

teacher=Teachers(name="teacher_4",_id=random.randint(1,100000),password="pass#teacher_4",classes=[{"class_9":"science"}])
teacher.save()

teacher=Teachers(name="teacher_5",_id=random.randint(1,100000),password="pass#teacher_5",classes=[{"class_9":"Hindi"}])
teacher.save()

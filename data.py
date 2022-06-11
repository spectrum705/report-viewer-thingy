import random 
import os
import csv,os
from pathlib import Path
from pytest import mark
from report.models import Teachers, Students, Marks#, Subjects
from report.helper import subject_list
from report import db


# csv file name
def createDb():
    # learn about relative path and absolute path
    folder = Path("report/school_data")
    data_file = folder/"student_dummy_data.csv"
    # data_file = r"C:\Users\SHUBHAM\Desktop\report-viewer-thingy\report\school_data\student_dummy_data.csv"
    with open(data_file, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
    #    write example of row
        for row in csvreader:
            if row[0].lower() != 'admission number':
                # enc_password = bcrypt.generate_password_hash( "pass#"+row[0].lower()).decode('utf-8')
                # {"admission_no": 4, "name": "four", "marks": {
                    #                                 "maths":{"test_1": None, "test_2": None, "test_3": None, "test_4": None, "grade": None},"},
                    #                                 "english":{"test_1": None, "test_2": None, "test_3": None, "test_4": None, "grade": None},"},
                    #                                 "science":{"test_1": None, "test_2": None, "test_3": None, "test_4": None, "grade": None},"},
                    #                                 }
                    # }, 
                    # restructure the db
                # student = Students(_id= int(row[0]), name=row[1], standard=row[2] ,marks=Marks(test_1=subject_list[row[2]],test_2=subject_list[row[2]],test_3=subject_list[row[2]],test_4=subject_list[row[2]]))
                student = Students(_id= int(row[0]), name=row[1], standard=row[2] )
                marks=Marks()
                for subject in subject_list[row[2]]:
                    # marks[subject]={"test_1":None, "test_2":None, "test_3":None, "test_4":None, "grade":None}
                    marks[subject]={"test_1":12, "test_2":31, "test_3":32, "test_4":41, "grade":None}
                                        
                student.marks= marks

                
                
                student.save()
                
                print(f"name: {row[1]}, class: {row[2]}, added")
    # os.remove(data_file)
    return True

Teachers.drop_collection()
Students.drop_collection()
createDb()
teacher=Teachers(name="teacher_1",_id=random.randint(1,100000),password="pass#teacher_1",classes=[{"class_9":"english"},{"class_4":"maths"},{"class_2":"hindi"}],)
teacher.save()

teacher=Teachers(name="teacher_2",_id=random.randint(1,100000),password="pass#teacher_2",classes=[{"class_9":"maths"}], isAdmin=True)
teacher.save()

teacher=Teachers(name="teacher_3",_id=random.randint(1,100000),password="pass#teacher_3",classes=[{"class_9":"social studies"}])
teacher.save()

teacher=Teachers(name="teacher_4",_id=random.randint(1,100000),password="pass#teacher_4",classes=[{"class_9":"science"}])
teacher.save()

teacher=Teachers(name="teacher_5",_id=random.randint(1,100000),password="pass#teacher_5",classes=[{"class_9":"Hindi"}])
teacher.save()



import random 
import os
import csv,os
from pathlib import Path
from report.models import Teachers, Students, Marks#, Subjects
from report.helper import Password, subject_list
from report import db


def make_student_object(id,name, standard):
    student = Students(_id= int(id), name=name.upper().strip(), standard=standard)
    marks=Marks()
    for subject in subject_list[standard]:
        # marks[subject]={"test_1":None, "test_2":None, "test_3":None, "test_4":None, "grade":None}
        marks[subject]={"test_1":10, "test_2":10, "test_3":10, "test_4":10, "grade":"A2"}
        # marks[subject]={"test_1":None, "test_2":None, "test_3":None, "test_4":None, "grade":None}
    student.marks= marks  
    student.save()

# teacher=Teachers(name="teacher_1",_id=random.randint(1,100000),password="pass#teacher_1",classes=[{"class_9":"english"},{"class_4":"maths"},{"class_2":"hindi"}],)

def make_teacher_object(id,name, classes=None ):
    pwd=f"pass#{name.lower()}"
    print(f"pwd:{pwd}")
    enc=Password.enc(pwd)
    # print("enC:",enc)
    teacher = Teachers(_id= int(id), name=name.upper().strip(), classes=classes, password=enc)

    teacher.save()


# csv file name
def create_studentDb():
    # learn about relative path and absolute path
    folder = Path("report/school_data")
    data_file = folder/"student_data.csv"
    # data_file = r"C:\Users\SHUBHAM\Desktop\report-viewer-thingy\report\school_data\student_dummy_data.csv"
    Students.drop_collection()

    with open(data_file, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
    #    write example of row

        for index, row in enumerate(csvreader):
#            if row[0].lower() != 'teacher id':
            if index != 0:
      
                # student.save()
                make_student_object(id=row[0], name=row[1], standard=row[2])
                print(f"name: {row[1]}, class: {row[2]}, added")
    os.remove(data_file)
    return True

def create_teacherDb():
    folder = Path("report/school_data")
    data_file = folder/"teacher_data.csv"
    # data_file = r"C:\Users\SHUBHAM\Desktop\report-viewer-thingy\report\school_data\student_dummy_data.csv"
    Teachers.drop_collection()
    enc=Password.enc("admin")
    admin=Teachers(name="ADMIN", _id=10000, isAdmin=True, password=enc)
    admin.save()
    print(">>ADMIN ADDED")

    with open(data_file, 'r') as csvfile:
        # creating a csv reader object
    # csvfile=open(data_file, 'r')
        csvreader = csv.reader(csvfile)
        #    write example of row
        for index, row in enumerate(csvreader):
            # if row[0].lower() != 'teacher id':
            if index != 0:
                # class_9:English/class_10:Maths
                # ["class_9:English","class_10:Maths"]
                # print(f"row:{row}, index:{index}")
                teaching_classes=row[2].split('/')
                # print("classes:{classes}")

                classes=[]
                for cls in teaching_classes:
                    cls=cls.split(":")
                    cls={cls[0].strip():cls[1].strip().upper()}
                    # have to check classes with Enums
                    classes.append(cls)
                        
                
                make_teacher_object(id=int(row[0]), name=row[1], classes=classes)
                # print(">>",classes)
                # print(f"name: {row[1]}, class: {row[2]}, pwd:{row[1]}, added")
            os.remove(data_file)
        # return True


# create_studentDb()
# create_teacherDb()

# class_9:English/class_10:Maths
# teacher=Teachers(name="teacher_1",_id=random.randint(1,100000),password="pass#teacher_1",classes=[{"class_9":"english"},{"class_4":"maths"},{"class_2":"hindi"}],)
# teacher.save()

# teacher=Teachers(name="teacher_2",_id=random.randint(1,100000),password="pass#teacher_2",classes=[{"class_9":"maths"}])
# teacher.save()

# teacher=Teachers(name="teacher_3",_id=random.randint(1,100000),password="pass#teacher_3",classes=[{"class_9":"social studies"}])
# teacher.save()

# teacher=Teachers(name="teacher_4",_id=random.randint(1,100000),password="pass#teacher_4",classes=[{"class_9":"science"}])
# teacher.save()

# teacher=Teachers(name="teacher_5",_id=random.randint(1,100000),password="pass#teacher_5",classes=[{"class_9":"Hindi"}])
# teacher.save()

# teacher=Teachers(name="admin",_id=random.randint(1,100000),password="admin",isAdmin=True)
# teacher.save()


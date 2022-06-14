from crypt import methods
import json
from multiprocessing import dummy
import random
from flask import jsonify, render_template, render_template_string,request,url_for,redirect , session, flash, send_file
import py
from sqlalchemy import null
from report import app, db, bcrypt
from flask_wtf.csrf import CSRFProtect
from requests import sessions
import os
from io import BytesIO
from report.forms import CreateAccount, LoginForm, UploadForm, UpdateForm
from flask_login import login_user, current_user, logout_user, login_required
from fillDb import createDb
from report.models import Teachers, Students, Marks
from report import pymongo_client
from report.helper import grade_calculator, subject_list

csrf = CSRFProtect(app)
# create student dummy data json file
test_list=["test_1","test_2", "test_3", "test_4"]	
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
   },
   
   
     "class_9":{"students": [
         
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
                
                    {"admission_no": 3, "name": "thre", "marks": {
                                                    "test_1":{"maths": None, "english": None, "science": None},
                                                    "test_2":{"maths": None, "english": None, "science": None},
                                                    "test_3":{"maths": None, "english": None, "science": None},
                                                    "test_4":{"maths": None, "english": None, "science": None}
                                                    }
                    },
                
                    {"admission_no": 4, "name": "four", "marks": {
                                                    "test_1":{"maths": None, "english": None, "science": None},
                                                    "test_2":{"maths": None, "english": None, "science": None},
                                                    "test_3":{"maths": None, "english": None, "science": None},
                                                    "test_4":{"maths": None, "english": None, "science": None}
                                                    }
                    },      
                    
                    # {"admission_no": 4, "name": "four", "marks": {
                    #                                 "maths":{"test_1": None, "test_2": None, "test_3": None, "test_4": None, "grade": None},"},
                    #                                 "english":{"test_1": None, "test_2": None, "test_3": None, "test_4": None, "grade": None},"},
                    #                                 "science":{"test_1": None, "test_2": None, "test_3": None, "test_4": None, "grade": None},"},
                    #                                 }
                    # },                   
                ]
   },
   
   
}
                    
teacher_dummy_data={
    "teacher_1":{
                "teacher_id": 1,
                "password":"pass#teacher_1",
                "classes":[{"class_1":"english"}                              
                         ]      
                },
    
    "teacher_2":{
                "teacher_id": 2,
                "password":"pass#teacher_2",
                 "classes":[{"class_1":"english"}, 
                            {"class_2":"science"},              
                         ]                     
                }  
}



@app.route('/class_navigation')
def class_navigation():
    print(">>>>>>>>",session["user"]["id"])
    username= session["user"]["name"] #get from login idp
    teacher_subjects=Teachers.objects(_id =session["user"]["id"]).first().classes
    # print(Teachers.objects(_id =).first().classes)    
    return render_template('class_navigation.html', classes=teacher_subjects, test_list=test_list)


@app.route('/admin_navigation')
def admin_navigation():
    print(">>>>>>>>",session["user"]["id"])
    user=Teachers.objects(_id =session["user"]["id"]).first()
    
    # print(Teachers.objects(_id =).first().classes)    
    if user.isAdmin:
        return render_template('admin.html', classes=subject_list.keys())
    else:
        return redirect(url_for('class_navigation'))


@app.route('/marks_entry/<standard>/<subject>/<test_name>', methods=['GET', 'POST'])
def upload_marks_page(standard, subject, test_name):
    
    # student_list  = student_dummy_data[standard]["students"]
    student_list = Students.objects(standard=standard)
    # print(student_list)
    if request.method == 'POST':
        # if all data not filled then show error
        db=pymongo_client.test
        student_database=db.students
        for student in  Students.objects(standard=standard):
            print(">>>studnet:", student.id)
         
            print("makrs from fromr:", request.form[str(student.id)])

           
            student_database.update_one({'_id':student.id}, {"$set":{f"marks.{subject}.{test_name}": int(request.form[str(student.id)])}}, upsert=False)
            # if all the test marks are filled update the student's main grade
           
            #  {"admission_no": 4, "name": "four", "marks": {
                    #                                 "maths":{"test_1": None, "test_2": None, "test_3": None, "test_4": None, "grade": None},"},
                    #                                 "english":{"test_1": None, "test_2": None, "test_3": None, "test_4": None, "grade": None},"},
                    #                                 "science":{"test_1": None, "test_2": None, "test_3": None, "test_4": None, "grade": None},"},
                    #                                 }
                    # }, 
            if list(student["marks"][subject].values()).count(None)==1:
                print(">>> adding grade")
                test_scores= [student["marks"][subject][test] for test in test_list]
                student_database.update_one({'_id':student.id}, {"$set":{f"marks.{subject}.grade": grade_calculator(test_scores)}}, upsert=False)
                if not None in [student["marks"][sub]["grade"] for sub in subject_list[student.standard]]:
                    student.isGraded=True
                    
                # student.update(grade="A1") #calculate using the grade funtion, by avegrading the marks of all the tests
                # print(f">>>>>student grdade updated:{student.name}", student.grade)
            
        # return redirect(url_for('class_result', standard=standard))
        flash("Marks uploaded successfully","info")
        return redirect(url_for('class_navigation'))
            
    return render_template('upload_marks.html', subject=subject, test_name=test_name, standard=standard, student_list=student_list)
    #return render_template('class_test.html')

@app.route('/class_result/<standard>')
def class_result(standard):
    student_list=Students.objects(standard=standard)
    subjects=list(subject_list[standard])
    return render_template('class_result.html', student_list=student_list, test_list=test_list, subject_list=subjects, standard=standard)
 
 
@app.route('/test')
def test():
    student=Students.objects(_id=1039).first()
    pic_src=f"https://avatars.dicebear.com/api/bottts/{student.id}.svg"
    return render_template('test.html', student=student, src=pic_src)

 
@app.route('/get_chart_data') 
def get_chart_data():
    student=Students.objects(_id=session["id_for_chart"]).first()
    subjects=list(subject_list[student.standard])
    test1_marks=[]
    test2_marks=[]
    test3_marks=[]
    test_4_marks=[]
    # print(">>>>>API Called",)
    for test in test_list:
        
        # print(">>>>>test:", test)
        for sub in subjects:
            # maths_ test1, englist_test1, science_test1, 
            if test == "test_1":
                test1_marks.append(student["marks"][sub][test])
            if test == "test_2":
                test2_marks.append(student["marks"][sub][test])
            if test == "test_3":
                test3_marks.append(student["marks"][sub][test])
            if test == "test_4":
                test_4_marks.append(student["marks"][sub][test])

    
    data={
        "chart_1":{"tags":subjects, "marks":test1_marks,"title":"Test 1","elementId":"myChart"},
        "chart_2":{"tags":subjects, "marks":test2_marks,"title":"Test 2","elementId":"myChart2"},
        "chart_3":{"tags":subjects, "marks":test3_marks,"title":"Test 3","elementId":"myChart3"},
        "chart_4":{"tags":subjects, "marks":test_4_marks,"title":"Test 4","elementId":"myChart4"}
        
    }
    
    
    # print(">>>>>data:", data)
    return jsonify(data)
    
@app.route('/student_dashboard/<id>')
def student_dashboard(id):
    session["id_for_chart"] = id
    student=Students.objects(_id=id).first()
    pic_src=f"https://avatars.dicebear.com/api/bottts/{student.id}.svg"
    return render_template('dashboard.html', student=student, src=pic_src)
    

  
@app.route('/report/<id>')
def report_card(id):
    session["student_id_for_chart"]=id
    student=Students.objects(_id=id).first()
    # print(">>> grade",student.grade)

    sub_list=list(subject_list[student.standard])
    # return render_template('report.html', student=student, subject_list=sub_list, standard=student.standard)
    
    # if not None in [student["marks"][sub]["grade"] for sub in subject_list[student.standard]]:
    return render_template('report.html', student=student, subject_list=sub_list, standard=student.standard)
    # else:
    #     flash("All the Marks are not entered", "danger")
    #     return redirect(url_for('class_result', standard=student.standard))



#admin page to edit user data
@app.route("/admin", methods = ["POST", "GET"])
def admin():
    usr = None
    form  = UpdateForm()
    
    if request.method == "POST":
        if request.form["admin"]:
            session['toUpdate'] = request.form["admin"]
            usr = User.query.filter_by(username = session['toUpdate']).first()
            print(request.form["admin"])
            if usr:
                form.username.data = usr.username
                form.theClass.data = usr.theClass
                form.userType = usr.userType
            else:
                return render_template("admin.html", result = usr, form = form)
            # return url_for("admin")

        elif form.validate_on_submit(): 
            print("valid now")
            updateUsr = User.query.filter_by(username = session['toUpdate']).first()
            print("name_in_form:", form.username.data)
            updateUsr.username = form.username.data 
            updateUsr.theClass = form.theClass.data 

            db.session.commit()
            print("after update:",updateUsr.username)
            # print("got user admission_no:", request.form["userId"])
            flash("Data Updated Successfully", "success")

    classes=subject_list.keys()    
    return render_template("admin.html", result = usr, form = form, classes=classes)


#admin can ad dnew user
@app.route('/create', methods= ["POST", "GET"])      
def create():
    form = CreateAccount()
    if form.validate_on_submit():
        
        pwd = "pass#" +form.username.data.split(' ')[0]
        enc_password = bcrypt.generate_password_hash(pwd).decode('utf-8')
        user = User(username=form.username.data, password = enc_password,
        userType = request.form["accountType"], theClass = form.theClass.data)
        db.session.add(user)
        db.session.commit()
        flash("New User added to the Database", 'success')
            # print(f"pass: {pwd}, name:{form.username.data}, class:{form.theClass.data}, type:{request.form['accountType']}")
        return  redirect(url_for("create"))
          
    return render_template("create.html", title='Register', form = form)
    
    
       


#home page  for login
@app.route("/", methods= ["POST", "GET"])        
def login():
    # try:
    # if current_user.is_authenticated:
    #     if current_user.userType == "teacher":
    #         return redirect(url_for("uploadResult"))

    #     elif current_user.userType == "student":
    #             return redirect(url_for("studentReport"))

    #     elif current_user.userType == "admin":
    #         return redirect(url_for("admin"))
    form = LoginForm()

    if "user" in session:
        
        if Teachers.objects(_id=session["user"]["id"]).first().isAdmin:
            print(">>>user in session:", session["user"])	
            return redirect(url_for("admin_navigation"))
        else:
            return redirect(url_for("class_navigation"))
    # find why it says none type object wen yser is already logged in   
       

    if form.validate_on_submit():
        # user = User.query.filter_by(username=form.username.data).first()
        # # theClass = User.query.filter_by(username=form.username.data).first()
        # if user and bcrypt.check_password_hash(user.password, form.password.data):# and theClass.theClass == request.form["theClass"]:
        #     login_user(user,remember = form.remember.data)
        #     flash("Logged in Successfully", "success")
        #     if current_user.userType == "teacher":
        #         return redirect(url_for("uploadResult"))

        #     elif current_user.userType == "admin":
        #         return redirect(url_for("admin"))
        
        #     else:
        #         return redirect(url_for("studentReport"))

        user = Teachers.objects(name=form.username.data.lower().strip()).first()
       

        # print("urs:",form.username.data)
        # print("pwd:", form.password.data)
        # print("userinDb",user)
        # print("pwd:",user.password)
        # if user is not None and form.password.data.strip() == user.password:
        if user is not None:
            session["user"] = user.to_json()#form.username.data
            login_user(user)
            session.permanent = True
            # set session experition after 4 hours i think
            # print("logged", current_user.username)
            flash("you are logged in ", "success")
            if Teachers.objects(_id=session["user"]["id"]).first().isAdmin:
                return  redirect(url_for("admin_navigation"))
                print(">>>user in session:", session["user"])	
            else:
                return redirect(url_for("class_navigation"))            
                    
        else:
            flash("Wrong username or password, check again.", "danger") 
    # except:
    #     return render_template("error.html")
  
    
    return render_template("login.html", title='Login', form = form)



#secure file upload or just make a function instead of a route
@app.route('/student_report/<getId>/<attach>', methods=["POST", "GET"])
@login_required
def download(getId, attach):
    # print( request.args.get("attach"))
    # print("download_stud-admission_no:",request.form["student_id"])
    user = User.query.filter_by(id = getId).first() 
    print(attach)
    print(user)
    return send_file(BytesIO(user.fileData), attachment_filename=user.fileName, as_attachment= attach )




@app.route("/student_report", methods=["GET"])   
@login_required     
def studentReport():
    # saving in file system
    # if current_user.fileName:
    #     with open(os.getcwd()+'/report/student_results/'+ f"{current_user.fileName}" ,'wb') as pen:
    #         pen.write(current_user.fileData)
    
    try:
        if current_user.userType == "student":
            report = User.query.filter_by(id = current_user.id).first()
            return render_template("student_report.html", file = report.fileName)
        elif current_user.userType == "teacher":
            return redirect(url_for("uploadResult"))
    except:
        return render_template("error.html")

    


@app.route("/upload_result", methods=["POST", "GET"])   
@login_required     
def uploadResult():
    try:
        form = UploadForm()
        if form.validate_on_submit():
            print("form submit validated")
            if form.resultFile.data:
                print("file has data rn")
                studentReport = User.query.filter_by(id = request.form["student_id"]).first()
                # resultFile = save_file(form.resultFile.data, name = studentReport.username )
                print("kid Id:", request.form["student_id"])
                studentReport.fileName = studentReport.username+"_result." + str(form.resultFile.data.filename).split('.')[1]#resultFile
                studentReport.fileData = form.resultFile.data.read()
                db.session.commit()
                flash("File Successfully Uploaded.", "success ")
                print("file uploaded:" )
            else:
                flash("Please select a file.", "danger")
        studentList = User.query.filter_by(userType="student", theClass = current_user.theClass).all()  
        if current_user.userType == "teacher":
            return render_template("upload_result.html", title="upload result", 
                            student = studentList,form=form)#, filename=filename)
        elif current_user.userType == "student":
            flash("huhuhuh, thought you were smarter kid?", "danger")
            return redirect(url_for("studentReport"))
        else:
            studentList = User.query.filter_by(userType="student").all()
            return render_template("upload_result.html", title="upload result", 
                            student = studentList,form=form)
    except:
        return render_template("error.html")



#function to save file 
def save_file(result_file):
    fileToSave = "all_data.csv"
    save_path = os.path.join(app.root_path, 'school_data',fileToSave)
    result_file.save(save_path)
    return fileToSave

#need to add steps to maake sure proper entry
#make sure admin data is mentioned
@app.route("/updateDb", methods=["POST", "GET"])   
def updateDatabase():
    form = UploadForm()
        # try:
    if form.validate_on_submit():
        save_file(form.resultFile.data)
        # flash("Please wait till we comeplete adding everything...", "success")
        createDb()
        flash("Database Creation Complete ! ", "success")
        print("file uploaded:" )
        return redirect(url_for("admin"))
    
    else:
        flash("Please select the file. After uploading it takes a while, So please wait...", "danger")   
    # except:
    #     return render_template("error.html")
    return render_template("updateDatabase.html", form = form)
    


@app.route("/logout")        
def logout():
    session.pop("user",None)
    # logout_user()
    return redirect(url_for("login"))

@app.route("/delete/<id>")   
@login_required     
def delete(id):
    if current_user.userType == "admin":
        User.query.filter_by(id=id).delete()
        db.session.commit()
        # print("usr deleted")
        flash("User deleted from the Database", "danger")
    return redirect(url_for("admin"))

    
    

    
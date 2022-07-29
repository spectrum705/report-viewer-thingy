
import json
from urllib import response

import requests
from sqlalchemy import true
#import pdfkit
import pandas as pd
import random
from flask import jsonify, make_response, render_template, render_template_string,request,url_for,redirect , session, flash, send_file
from report import app, db, bcrypt
#from flask_weasyprint import HTML, render_pdf
 
from flask_wtf.csrf import CSRFProtect
from requests import sessions
import os
from io import BytesIO
from report.forms import CreateAccount, LoginForm, UploadForm, UpdateForm
from flask_login import login_user, current_user, logout_user, login_required, user_logged_in
# from fillDb import createDb
from data import create_teacherDb, make_student_object, make_teacher_object, create_studentDb
from report.models import Teachers, Students, Marks
from report import pymongo_client
from report.helper import grade_calculator, subject_list, Password
import ast

csrf = CSRFProtect(app)
# create student dummy data json file
test_list=["test_1","test_2", "test_3", "test_4"]	
USER_TOKEN =None
student_dummy_data = {
  
   
   
     "class_9":{"students": [
         
                   
                    {"admission_no": 4, "name": "four", "marks": {
                                                    "maths":{"test_1": None, "test_2": None, "test_3": None, "test_4": None, "grade": None}},
                                                    "english":{"test_1": None, "test_2": None, "test_3": None, "test_4": None, "grade": None},
                                                    "science":{"test_1": None, "test_2": None, "test_3": None, "test_4": None, "grade": None},
                                                    }
                                    
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
@login_required
def class_navigation():

    print(">>>>>>>>",session["user"]["id"])
    username= session["user"]["name"] #get from login idp
    teacher_subjects=Teachers.objects(_id =session["user"]["id"]).first().classes
    # print(Teachers.objects(_id =).first().classes)    
    return render_template('class_navigation.html', classes=teacher_subjects, test_list=test_list)
    
# @app.route('/admin_navigation')
# @login_required
# def admin_navigation():
#     print(">>>>>>>>",session["user"]["id"])
#     user=Teachers.objects(_id =session["user"]["id"]).first()
    
#     # print(Teachers.objects(_id =).first().classes)    
#     if user.isAdmin:
#         return render_template('admin.html', classes=subject_list.keys())
#     else:
#         flash("Your account does not have admin rights","danger")
#         return redirect(url_for('class_navigation'))


#admin page to edit user data
@app.route("/admin_navigation", methods = ["POST", "GET"])
@login_required
def admin():
    usr = None
    form  = UpdateForm()
    print(">>>>>>>>",session["user"]["id"])
    user_logged=Teachers.objects(_id =session["user"]["id"]).first()
    if user_logged.isAdmin:
        if request.method == "POST":
            if request.form["admin"]:
                session['toUpdate'] = request.form["admin"]
                usr = Teachers.objects(name=(session['toUpdate'])).first() or Students.objects(name=session['toUpdate'].upper()).first() #User.query.filter_by(username = session['toUpdate']).first()
                print(request.form["admin"])
                # print(">>>>>>>>",usr.name)	

                if usr:
                    form.username.data = usr.name
             
                    try:
                        form.theClass.data = (usr.classes) 
                        form.userType="Teacher"
                    except:
                        pass
                    try:
                        form.theClass.data= (usr.standard)
                        form.userType="Student"

                    except:
                        pass
                    # form.userType = usr.userType
                else:
                    return render_template("admin.html", result = usr, form = form)
                # return url_for("admin")

            elif form.validate_on_submit(): 
                print("valid now")
                try:
                    updateUsr =  Teachers.objects(name=session['toUpdate']).first() 
                    updateUsr.modify(name=form.username.data, classes=ast.literal_eval(form.theClass.data))
                    print("name_in_form:", form.username.data)
                except:
                    pass
                try:
                    updateUsr= Students.objects(name=session['toUpdate']).first()
                    marks=Marks()
                    for subject in subject_list[form.theClass.data]:
                    # marks[subject]={"test_1":None, "test_2":None, "test_3":None, "test_4":None, "grade":None}
                        marks[subject]={"test_1":10, "test_2":10, "test_3":10, "test_4":10, "grade":"A2"}
                                            
                        # updateUsr.marks= marks
                    updateUsr.modify(name=form.username.data, standard=form.theClass.data, marks=marks)
                except:
                    pass
                
                    # for student
               
                # updateUsr.theClass = form.theClass.data 

                # print("got user admission_no:", request.form["userId"])
                flash("Data Updated Successfully", "success")

        classes=subject_list.keys()    
        return render_template("admin.html", result = usr, form = form, classes=subject_list.keys())

    else:
        flash("Your account does not have admin rights","danger")
        return redirect(url_for('class_navigation'))




@app.route('/marks_entry/<standard>/<subject>/<test_name>', methods=['GET', 'POST'])
@login_required
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
            if list(student["marks"][subject].values()).count(None)==1:
                print(">>> adding grade")
                test_scores= [student["marks"][subject][ test] for test in test_list]
                student_database.update_one({'_id':student.id}, {"$set":{f"marks.{subject}.grade": grade_calculator(test_scores)}}, upsert=False)
                if not None in [student["marks"][sub]["grade"] for sub in subject_list[student.standard]]:
                    student.isGraded=True
                    
                # student.update(grade="A1") #calculate using the grade funtion, by avegrading the marks of all the tests
                # print(f">>>>>student grdade updated:{student.name}", student.grade)
            
        # return redirect(url_for('class_result', standard=standard))
        flash("Marks uploaded successfully","info")
        return redirect(url_for('class_navigation'))
            
    return render_template('upload_marks.html', subject=subject, test_name=test_name, standard=standard, student_list=student_list)




# TODO
@app.route(f'/class_result/<standard>', methods=["GET","POST"])
@login_required
def class_result(standard):
    # print("USERTOKEN IN CLS RESLUT:", USER_TOKEN)
  
    student_list=Students.objects(standard=standard)
    subjects=list(subject_list[standard])
    # Making class marksheet download
    if request.method=="POST":
        
        table = pd.read_html ( render_template('class_result.html', student_list=student_list, test_list=test_list, subject_list=subjects, standard=standard))[ 0 ]
        sheet = table .to_excel (f"{standard}_marsheet.xlsx" )
        flash("Marksheet downloaded", "info")
        return send_file(BytesIO(sheet), attachment_filename=f"{standard}_marsheet.xlsx", as_attachment=True)
    return render_template('class_result.html', student_list=student_list, test_list=test_list, subject_list=subjects, standard=standard)
   
# @app.route('/student_report/<getId>/<attach>', methods=["POST", "GET"])
# @login_required
# def download(getId, attach):
#     # print( request.args.get("attach"))
#     # print("download_stud-admission_no:",request.form["student_id"])
#     user = User.query.filter_by(id = getId).first() 
#     print(attach)
#     print(user)
#     return send_file(BytesIO(user.fileData), attachment_filename=user.fileName, as_attachment= attach )


 

# @app.route(f'/class_result/<standard>/get-data/{Config.objects(name="marksheet_code").first().code}')
# def marksheet_download(standard, code):
#     student_list=Students.objects(standard=standard)
#     subjects=list(subject_list[standard])
#     print(">>>>download page:", code)
#     flash("Class marksheet Downloaded", "info")    

#     # Config.objects(name="marksheet_code").first().delete()
#     return render_template('class_result.html', student_list=student_list, test_list=test_list, subject_list=subjects, standard=standard)
   
 
@app.route('/test')
@login_required                                                  
def test():
    form = UploadForm()
 
    return render_template('error.html')


@app.route('/get_chart_data') 
def get_chart_data():
    student=Students.objects(_id=session["id_for_chart"]).first()
    subjects=list( subject_list[student.standard])
    test1_marks=[]
    test2_marks=[]
    test3_marks=[]
    test4_marks=[]
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
                test4_marks.append(student["marks"][sub][test])

    
    data={
        "chart_1":{"tags":subjects, "marks":test1_marks,"title":"Test 1","elementId":"myChart"},
        "chart_2":{"tags":subjects, "marks":test2_marks,"title":"Test 2","elementId":"myChart2"},
        "chart_3":{"tags":subjects, "marks":test3_marks,"title":"Test 3","elementId":"myChart3"},
        "chart_4":{"tags":subjects, "marks":test4_marks,"title":"Test 4","elementId":"myChart4"}
        
    }
    session.pop("id_for_chart", None)
    # print(">>>>>data:", data)
    return jsonify(data)

@app.route('/student_dashboard/<id>')
@login_required
def student_dashboard(id):
    session["id_for_chart"] = id
    student=Students.objects(_id=id).first()
    pic_src=f"https://avatars.dicebear.com/api/bottts/{student.id}.svg"
    return render_template('dashboard.html', student=student, src=pic_src)
    

@app.route('/report/<id>')
@login_required
def report_card(id):
    session["student_id_for_chart"]=id
    student=Students.objects(_id=id).first()
    # print(">>> grade",student.grade)

    sub_list=list(subject_list[student.standard])
   
    if student.isGraded:

        # TODO
        # rendered= render_template('report.html', student=student, subject_list=sub_list, standard=student.standard)
        # pdf =pdfkit.from_string(rendered,False)
        
        # response=make_response(pdf)
        # response.headers['Content-Type']='application/pdf'
        # response.headers['Content-Disposition']='attachment; filename=report_card.pdf'
        flash("Report Card Downloaded",'info')
        # return response
        # return send_file((rendered), attachment_filename='output.pdf', as_attachment= True )

        return render_template('report.html', student=student, subject_list=sub_list, standard=student.standard)
    else:
        flash("All the Marks are not entered", "danger")
        return redirect(url_for('class_result', standard=student.standard))

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



#admin can ad dnew user
@app.route('/create', methods= ["POST", "GET"])    
@login_required  
def create():
    form = CreateAccount()
    if current_user.isAdmin:
        if form.validate_on_submit():
            # enc_password = bcrypt.generate_password_hash(pwd).decode('utf-8')
            if request.form["accountType"] == "student":       
                make_student_object(id=form.id.data, name=form.username.data, standard=form.theClass.data,)
                flash("New User added to the Database", 'success')
                # print(f"pass: {pwd}, name:{form.username.data}, class:{form.theClass.data}, type:{request.form['accountType']}")
            else:
                make_teacher_object(id=form.id.data, name=form.username.data, classes=ast.literal_eval(form.theClass.data))
                flash("New User added to the Database", 'success')
            
            return  redirect(url_for("create"))
            
        return render_template("create.html", title='Register', form = form)
    else:
        return redirect(url_for("login"))
        
    
       


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

    if current_user.is_authenticated:
        
        if Teachers.objects(_id=session["user"]["id"]).first().isAdmin:
            print(">>>user in session:", session["user"])	
            return redirect(url_for("admin"))
        else:
            return redirect(url_for("class_navigation"))
    # find why it says none type object wen yser is already logged in   
       

    if form.validate_on_submit():

        user = Teachers.objects(name=form.username.data.upper().strip()).first()
       
        # print(f"pwd form:{form.password.data}, pwd usr:{user.password}, check:{Password.check(pwd_entered=form.password.data.strip(),hashed_pwd= user.password)}")
        # if (user is not None) and Password.check(pwd_entered=form.password.data.strip(),hashed_pwd= user.password):
            # print("")
       
        if user is not None:
            session["user"] = user.to_json()#form.username.data
            
            login_user(user)
            print(">>>>>current user", current_user.classes)
            session.permanent = True
            # set session experition after 4 hours i think
            # print("logged", current_user.username)
            flash("you are logged in ", "success")
            if Teachers.objects(_id=session["user"]["id"]).first().isAdmin:
                return  redirect(url_for("admin"))
                print(">>>user in session:", session["user"])	
            else:
                return redirect(url_for("class_navigation"))            
                    
        else:
            flash("Wrong username or password, check again.", "danger") 
    # except:
    #     return render_template("error.html")
  
    
    return render_template("login.html", title='Login', form = form)







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

@app.route('/info')
def info():
    return render_template('db_info.html')

#function to save file 
def save_file(result_file, file_name):
    fileToSave = file_name
    isExist = os.path.exists('report/school_data')
    if not isExist:
        os.makedirs('report/school_data')
    save_path = os.path.join(app.root_path, 'school_data',fileToSave)
    result_file.save(save_path)
    return fileToSave

#need to add steps to maake sure proper entry
#make sure admin data is mentioned
@app.route("/updateDb", methods=["POST", "GET"])   
def updateDatabase():
    teacher_data_form = UploadForm()
    student_data_form = UploadForm()
    form=UploadForm()
        
    # try:
    flash("Please select the right file. After uploading it takes a while, So please wait...", "yellow")   
    if request.method == "POST":
        form_name = request.form['form_name']
        if form_name == 'teacher_form':
    # if teacher_data_form.validate_on_submit():
            save_file(teacher_data_form.resultFile.data, file_name="teacher_data.csv")
            # flash("Please wait till we comeplete adding everything...", "success")
            create_teacherDb()
            flash("Database Creation Complete ! ", "success")
            print("file uploaded:" )
            return redirect(url_for("admin"))
        elif form_name == 'student_form':

    # if student_data_form.validate_on_submit():
            save_file(student_data_form.resultFile.data, file_name = "student_data.csv")
            # flash("Please wait till we comeplete adding everything...", "success")
            create_studentDb()
            flash("Database Creation Complete ! ", "success")
            print("file uploaded:" )
            return redirect(url_for("admin"))
    
    
    # except:
    #     flash("Something went wrong, check everything again","danger")
    #     return render_template("error.html")
    return render_template("updateDatabase.html", student_form = student_data_form, teacher_form=teacher_data_form, form=form)
    


@app.route("/logout")        
def logout():
    session.pop("user",None)
    logout_user()
    return redirect(url_for("login"))

@app.route("/delete/<id>")   
@login_required     
def delete(id):
    if current_user.isAdmin:
        user= Teachers.objects(_id=id).first() or Students.objects(_id=id).first()
        user.delete()
        # print("usr deleted")
        flash("Record deleted from the Database", "danger")
    return redirect(url_for("admin"))

    
    

# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template('error.html'),404
 
# #Handling error 500 and displaying relevant web page
# @app.errorhandler(500)
# def internal_error(error):
#     return render_template('error.html'),500

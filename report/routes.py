from flask import render_template,request,url_for,redirect , session, flash
from report import app, db, bcrypt
from requests import sessions
from report.models import User
from report.forms import CreateAccount, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

grades = ["lkg", "ukg", "1","2","3","4","5","6","7","8","9","10"]

# @app.route('/', methods=["POST", "GET"])
# def home():
    
#         return render_template("index.html")



@app.route('/create', methods= ["POST", "GET"])      
def create():
    # if current_user.is_authenticated:
    #    return redirect(url_for("home"))
    form = CreateAccount()
    if form.validate_on_submit():
        enc_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password = enc_password, userType = request.form["accountType"])
        db.session.add(user)
        db.session.commit()
        flash(f'Woohoo! Welcome {form.username.data} !', 'success')
        return  redirect(url_for("login"))
    return render_template("create.html", title='Register', form = form, grade = grades)

@app.route("/", methods= ["POST", "GET"])        
def login():
    if current_user.is_authenticated:
        if current_user.userType == "teacher":
            return redirect(url_for("uploadResult"))

        elif current_user.userType == "student":
                return redirect(url_for("studentReport"))

    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        theClass = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):# and theClass.theClass == request.form["theClass"]:
            login_user(user,remember = form.remember.data)
            flash("you are logged in ", "success")
            if current_user.userType == "teacher":
                return redirect(url_for("uploadResult"))
            else:
                return redirect(url_for("studentReport"))
            
                    
        else:
            flash("Wrong username or password or the class, check again.", "danger") 
    return render_template("login.html", title='Login', form = form)




@app.route("/student_report", methods=["POST", "GET"])   
@login_required     
def studentReport():
    # collection = UserShow.query.filter_by(user_id=current_user.id).all()  
    # return render_template("mycollection.html", title= "My Collection", collection = collection)
    return render_template("student_report.html")


@app.route("/upload_result", methods=["POST", "GET"])   
@login_required     
def uploadResult():
    # collection = UserShow.query.filter_by(user_id=current_user.id).all()  
    # return render_template("mycollection.html", title= "My Collection", collection = collection)
    studentList = User.query.filter_by(userType="student", theClass = current_user.theClass).all()  
    return render_template("upload_result.html", title="upload result",  student = studentList)




@app.route("/delete" ,methods=["POST","GET"])   
def delete():

   return "gotta add the delete report method"

@app.route("/logout")        
def logout():
    logout_user()
    return redirect(url_for("login"))
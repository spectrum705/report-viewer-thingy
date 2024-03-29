from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField

from wtforms.validators import DataRequired,Length, EqualTo, ValidationError
from report.models import Teachers
from flask_wtf.file import FileField,FileAllowed

#will delete this later
class CreateAccount(FlaskForm):
    username = StringField('Username',
                             validators=[DataRequired(),
                            Length(min = 3, max= 15 ) ])
   
    theClass =  TextAreaField('class',
                            validators = [DataRequired()],  render_kw={"placeholder": "write teacher's classes in the following way:         [{'class_9':'english'},{'class_4':'maths'},]"})
    
    id = IntegerField('id', validators=[DataRequired()])

   
    submit = SubmitField('confirm')
    def validate_username(self, username):
        user = Teachers.objects(name=username.data).first()
        if user:
            raise ValidationError('Username taken, think of another.')        


class LoginForm(FlaskForm):
    username = StringField('Username',
                             validators=[DataRequired(),
                            Length(min = 3, max= 15 ) ])
    password = PasswordField('Password', 
                            validators = [DataRequired()])
    
    
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


class UploadForm(FlaskForm):

    resultFile = FileField(label ='upload the result', validators= [FileAllowed(['pdf', 'jpg','csv'])] )
    submit = SubmitField('upload')
class UpdateForm(FlaskForm):
    csrf = True
    username = StringField('Username')
    theClass = TextAreaField('Classes')
    userType = StringField('User Type')

    submit = SubmitField('Update')
    


# # Panda import
# import pandas as pd

  
# # URL of the web page whose table we want to extract
# url = "/class_result/class_9"
  
# # Assign table data to Pandas dataframe
# table = pd.read_html (url) [ 0 ]
  
# # Print data frame
# print (table)

# # ---------------------------------------------------------------------
# Pandas import
import pandas as pd
from report.models import Students, Marks, Teachers
from flask import render_template, redirect, url_for, flash, request, Flask 
from report.helper import subject_list
 
# URL of the web page whose table we want m extract
# @app.route('/class_result/<standard>')
# app = Flask(__name__)
def class_result(standard):
    student_list=Students.objects(standard=standard)
    subjects=list(subject_list[standard])
    temp = render_template('class_result.html', student_list=student_list, test_list=test_list, subject_list=subjects, standard=standard)
   
# Assign table data to a Pandas dataframe
    table = pd.read_html (temp) [ 0 ]

 
# Save data frame to Excel file
    table .to_excel ( "report_card.xlsx" )
class_result("class_9")
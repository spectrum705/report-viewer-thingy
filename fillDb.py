from report import db, bcrypt
from report.models import User
import csv

  
# csv file name
db.create_all()
filename = "dummy.csv"
# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
    
    for row in csvreader:
        if row[0] != 'username':
            enc_password = bcrypt.generate_password_hash( "pass#"+row[0]).decode('utf-8')
            usr = User (username = row[0], userType = row[2],
                         theClass = str(row[1]), password=enc_password )
            db.session.add(usr)
            db.session.commit()

            
            print(f"name: {row[0]}, class: {row[1]}, type: {row[2]} added")

     # from report.models import db, User

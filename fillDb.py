from report import db, bcrypt
from report.models import Teachers
import csv,os
from pathlib import Path
  
# csv file name
def createDb():
    folder = Path("report/school_data")
    data_file = folder/"all_data.csv"
    # filename = "all_data.csv"
    db.drop_all()
    db.create_all()
    # reading csv file
    with open(data_file, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        #example of entry in file 
        #username theClass userType
        #student1   7      student
        for row in csvreader:
            if row[0].lower() != 'username':
                enc_password = bcrypt.generate_password_hash( "pass#"+row[0].lower()).decode('utf-8')
                usr = User(username = row[0].lower(), userType = row[2].lower(),
                            theClass = str(row[1]), password=enc_password )
                db.session.add(usr)

                
                print(f"name: {row[0]}, class: {row[1]}, type: {row[2]} added")
        db.session.commit()
    os.remove(data_file)
    return True
# from report.models import db, User
# from report import db, bcrypt
# db.drop_all()
# db.create_all()
# pwd = bcrypt.generate_password_hash( "test").decode('utf-8')
# usr =User(username ="kami", userType = "admin", theClass = "", password=pwd )
# db.session.add(usr)
# db.session.commit()

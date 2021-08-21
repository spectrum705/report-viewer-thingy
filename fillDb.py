from report import db, bcrypt
from report.models import User
import csv,os

  
# csv file name
def createDb():
    db.drop_all()
    db.create_all()
    filename = "all_data.csv"
    # reading csv file
    with open( os.getcwd() +'/report/school_data/'+filename, 'r') as csvfile:
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
                db.session.commit()

                
                print(f"name: {row[0]}, class: {row[1]}, type: {row[2]} added")
        os.remove(os.getcwd() +'/report/school_data/'+filename)
    return True
     # from report.models import db, User

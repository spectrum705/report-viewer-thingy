from report import db, bcrypt
from report.models import User

#do python3 fillDb.py to make test users (7 teachers and students)

for i in range(1,7):
    enc_password = bcrypt.generate_password_hash( "sss"+str(i)).decode('utf-8')
    usr = User (username = "student"+str(i), userType = "student",
                 theClass = str(i), password=enc_password )
    db.session.add(usr)
    db.session.commit()


for i in range(1,7):
  
    enc_password = bcrypt.generate_password_hash("ttt"+str(i)).decode('utf-8')
    usr = User (username = "teacher"+str(i), userType = "teacher",
                 theClass = str(i), password=enc_password  )
    db.session.add(usr)
    db.session.commit()

print("users: " , User.query.all())
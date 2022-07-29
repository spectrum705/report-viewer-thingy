# subject_names to be made from enumes
# from passlib.hash import bcrypt
import bcrypt
import enum

    # sub names to be made from Enums 

class Subjects(str, enum.Enum):
    eng="English",
    hindi="Hindi",
    sans="Sanskrit",
    sci="Science",
    maths="Maths",
    phy="Physics",
    chem="Chemistry",
    history="History",
    geo="Geography",
    politics="Political Science",
    social_sci="Social Science",
    
    
subject_list={ "class_9":[Subjects["maths"].value.upper(), Subjects["eng"].value.upper(), Subjects["sci"].value.upper(), Subjects["phy"].value.upper(), Subjects["chem"].value.upper()],
                "class_8":[Subjects["maths"].value.upper(),Subjects["history"].value.upper(),Subjects["geo"].value.upper()],
                "class_10":[Subjects["maths"].value.upper(), Subjects["eng"].value.upper(), Subjects["sci"].value.upper(), Subjects["social_sci"].value.upper()],
                
                "class_5":[Subjects["maths"].value.upper(),Subjects["history"].value.upper(),Subjects["geo"].value.upper()],

                }

# GradeEnum[grade].value
# class GradeEnum(str, enum.Enum):
#     A = 'A'
#     B = 'B'
#     C = 'C'
#     D = 'D'
    
# import bcrypt
# username = request.form.get("username")
# password = request.form.get("password").encode("utf-8")
# hashed = bcrypt.hashpw(password,bcrypt.gensalt())
# # Look user up in DB using username
# if bcrypt.checkpw(password, hashed):
#     print("It matches!")
# else:
#     print("Didn't match")
# ye dkhlena

class Password:
    # hasher = bcrypt.using(rounds=11)  # Make it slower
    @classmethod
    def enc(cls,pwd):
        # hashed_password= Password.hasher.hash(pwd)
        hashed_password = bcrypt.hashpw(pwd.encode("utf-8"),bcrypt.gensalt())
        return hashed_password

    @classmethod
    def check(cls,pwd_entered, hashed_pwd):
        return bcrypt.checkpw(pwd_entered.encode("utf-8"), hashed_pwd)
        # return Password.hasher.verify(pwd_entered, hashed_pwd)
    
    
class TestNames(str, enum.Enum):
    test_1="Test 1"
    


# enumaratetion of grades
class GradeEnum(str, enum.Enum):
    A1 = 'A1'
    A2 = 'A2'
    B1 = 'B1'
    C1 = 'C1'
    C2 = 'C2'
    D1 = 'D1'
    D2 = 'D2'
    E1 = 'E1'
    E2 = 'E2'
    F = 'F'
 
 

def grade_calculator(marks):
    return "A1->Function to be written"
    
    # avg = sum(marks)/len(marks)
    # if avg>=91:
    #     return GradeEnum["A1"].value
    # elif avg>=81:
    #     return GradeEnum["A2"].value
    # elif avg>=71:
    #     return GradeEnum["B1"].value
    # elif avg>=61:
    #     return GradeEnum["B2"].value
    # elif avg>=51:
    #     return GradeEnum["C1"].value
    # elif avg>=41:
    #     return GradeEnum["C2"].value
    # elif avg>=33:
    #     return GradeEnum["D1"].value
    # elif avg>=21:
    #     return GradeEnum["E1"].value
    # else:
    #     return GradeEnum["E2"].value
     
    
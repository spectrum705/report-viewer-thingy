# subject_names to be made from enumes

import enum

    # sub names to be made from Enums 

class Subjects(str, enum.Enum):
    eng="English",
    sci="Sci",
    

subject_list={ "class_9":["maths", Subjects.eng, Subjects.sci, "french", "japanese"],
                "class_8":["maths","ecology","history","geography","social"],
                "class_10":["maths","english","science","social"]
                }

class GradeEnum(str, enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    
class TestNames(str, enum.Enum):
    test_1="Test 1"
    


# enumaratetion of grades
class Grades(str, enum.Enum):
    A1 = 'A1'
    A2 = 'A2'
    B1 = 'B1'
    C1 = 'C1'
    C2 = 'C2'
    D = 'D'
    E1 = 'E1'
    E2 = 'E2'
    # F = 'F'
 
 

def grade_calculator(marks):
    return "A1->Function to be written"
    # avg = sum(marks)/len(marks)
    # if avg >= 91:
    #     return 'A1'
    # elif avg >= 81:
    #     return 'A2'
    # elif avg >= 71:
    #     return 'B1'
    # elif avg >= 61:
    #     return 'B2'
    # elif avg >= 51:
    #     return 'C1'
    # elif avg >= 41:
    #     return 'C2'
    # elif avg >= 33:
    #     return 'D'
    # elif avg >= 21:
    #     return 'E1'
    # else:
    #     return 'E2'

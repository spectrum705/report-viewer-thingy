from report.models import Teachers, Students, Marks#, Subjects


data = []

students = Students.objects(standard="class_9")

for each in students:
    kid = {}
    marks={}
    kid["id"]=each.id
    kid["name"] = each.name
    for i in (each.marks):
        marks[i]=each.marks[i]
    kid["marks"]=marks
    kid["standard"]=each.standard
    data.append(kid)



print(data)


# from report.models import Teachers, Students, Marks#, Subjects
import requests

# data = []

# students = Students.objects(standard="class_9")

# for each in students:
#     kid = {}
#     marks={}
#     kid["id"]=each.id
#     kid["name"] = each.name
#     for i in (each.marks):
#         marks[i]=each.marks[i]
#     kid["marks"]=marks
#     kid["standard"]=each.standard
#     data.append(kid)



# print(data)

data = {'blood':'O+'}
res = requests.post('http://172.17.246.28:5002/', data=data)
    
print(res.text
      )

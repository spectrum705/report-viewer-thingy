
# Student Report Viewer

It simplifies the process of academic evalution of students and keeps track of the scores.

 

## Features

-       Teacher Account: Can enter marks for the students in their class
-       Admin Account: - Can see the class data
                       - Can edit, add and delete any Account
                       - Can View graphical representation of marks
                       - Can export Data


## Demo

Demo Accounts:

`Teacher_1`

`Admin`

[Deployed Demo Link](https://student-report-thingy.herokuapp.com)


## Run Locally

Clone the project

```bash
git clone https://github.com/animed705/report-viewer-thingy/
```

Go to the project directory

```bash
  cd report-viewer-thingy
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start the server

```bash
python run.py
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

Create a .env file inside /report and add URI of your mongodb Database 

`DB_URI =  "mongodb+srv://{Database_name}:{Database_pwd}@ourcluster.xjtv1.mongodb.net/test?retryWrites=true&w=majority"`




## Tech Stack

**Client:** HTML, CSS

**Server:** Flask

**Database:** MongoDB


## Screenshots

![Login Page](/Login.png)
![Class result](/class_result.png)
![Dashboard](/dashboard.png)

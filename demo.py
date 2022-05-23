#create flask app
from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def home():
    return "<h1> Hewllo humans </h1>"

@app.route('/about')
def about():
    return "<h3> about humans </h3>"
 
 

if __name__ == '__main__':
    app.run(debug=True)
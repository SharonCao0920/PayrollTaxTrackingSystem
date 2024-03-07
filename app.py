from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps
from flask import Flask, jsonify, redirect, render_template, request, session
import pymongo
from dotenv import load_dotenv
import os

from werkzeug import Client


app = Flask(__name__)  
app.secret_key = "secret"

#test
load_dotenv()
URI = os.getenv("DATABASE_URI")
#client = pymongo.MongoClient(URI)
#db = Client.get_database("user_login_system")


#database
client = pymongo.MongoClient(URI)
db = client.user_login_system

otp_collection = db.otp_collection


#decorators
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            return redirect('/')
        
    return wrap
#routes 
from user import routes
from generateOTP import routes
from calculateTax import routes

@app.route('/')
def home():
    return render_template('login.html')   


@app.route('/about')
def about():
    return render_template('about.html')   

@app.route('/services')
def services():
    return render_template('service.html') 

@app.route('/contact')
def contact():
    return render_template('contact.html') 

@app.route('/homepage')
def homepage():
    return render_template('home.html') 

# @app.route('/gologin')
# def gologin():
#     return render_template('login.html')  

@app.route('/gosignup/')
def goSignup():
    return render_template('signup.html')   

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')   

@app.route('/goforgetPass/')
def goforgetPass():
    return render_template('forgetpassword.html') 


@app.route('/goresetPass/')
def goresetPass():
    return render_template('resetpassword.html')

@app.route('/generate/')
def generate():
    return render_template('generateOTP.html')

@app.route('/calculate/')
def calculate():
    return render_template('calculateTax.html')

if __name__ == '__main__':
    app.run(debug=True)
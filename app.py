from functools import wraps
from flask import Flask, redirect, render_template, session
import pymongo
from dotenv import load_dotenv
import os 

app = Flask(__name__)  
app.secret_key = "secret"

load_dotenv()
URI = os.getenv("DATABASE_URI")

#database
client = pymongo.MongoClient(URI)
db = client.user_login_system

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

@app.route('/')
def home():
    return render_template('login.html')   


@app.route('/about')
def about():
    return render_template('about.html')   

@app.route('/services')
def services():
    return render_template('service.html') 

@app.route('/payrollcalculator')
def payrollcalculator():
    return render_template('payrollcalculator.html') 

@app.route('/contact')
def contact():
    return render_template('contact.html') 

@app.route('/homepage')
def homepage():
    return render_template('home.html')   

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
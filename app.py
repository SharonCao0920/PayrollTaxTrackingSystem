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

@app.route('/gosignup/')
def goSignup():
    return render_template('signup.html')   

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')    
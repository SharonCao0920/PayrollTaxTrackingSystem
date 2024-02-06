from flask import Flask, request, jsonify, render_template
import pymongo
from dotenv import load_dotenv
import os 

app = Flask(__name__)  

load_dotenv()
URI = os.getenv("DATABASE_URI")

#database
client = pymongo.MongoClient(URI)
db = client.user_login_system

#routes 
from user import routes

@app.route('/')
def home():
    return render_template('home.html')    

@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')    
from functools import wraps
from flask import Flask, redirect, render_template, session, url_for
import pymongo
from dotenv import load_dotenv
import os
from authlib.integrations.flask_client import OAuth
from datetime import timedelta


app = Flask(__name__)
app.secret_key = "secret"

load_dotenv()
URI = os.getenv("DATABASE_URI")

oauth = OAuth(app)
# Session config
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)


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

@app.route('/auth_google/')
def auth_google():
    google = oauth.create_client('google')
    redirect_uri = url_for('auth_google', _external=True)  # Redirect to this route for authorization
    return google.authorize_redirect(redirect_uri)

@app.route('/auth_google/authorized')
def auth_google_authorized():
    google = oauth.create_client('google')  # Create the Google OAuth client
    token = google.authorize_access_token()  # Access token from Google (needed to get user info)
    resp = google.get('userinfo')  # Userinfo contains stuff specified in the scope
    user_info = resp.json()
    # Here you use the profile/user data that you got and query your database to find/register the user
    # and set your own data in the session, not the profile from Google
    session['profile'] = user_info
    session.permanent = True  # Make the session permanent so it keeps existing after the browser gets closed
    return redirect('/')

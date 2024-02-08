from flask import Flask, request, jsonify, render_template
from app import app
from user.models import User

@app.route('/user/signup/', methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/signout/')
def signout():
    return User().signout()

@app.route('/user/login/', methods=['POST'])
def login():
    return User().login()

@app.route('/user/forgetpassword', methods=['POST'])
def forget_password():
    return User().forget_password()

# undo: /user/resetpassword/<token>
@app.route('/user/resetpassword', methods=['POST'])
def reset_password():
    return User().reset_password()
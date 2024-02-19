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


@app.route('/user/forgetPass/', methods=['POST'])
def forgetPass():
    return User().forgetPass()


@app.route('/user/resetPass/', methods=['POST'])
def resetPass():
    return User().resetPass()


@app.route('/user/comparePdf/', methods=['POST'])
def comparePdf():
    return User().comparePdf()

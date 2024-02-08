from flask import Flask, redirect, request, jsonify, session
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class User:
    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200
    
    def signup(self):
        print(request.form)
        
        #create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }
        
        #confirm password
        confirm_password = request.form.get('confirm_password')
        if user['password'] != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400
        
        # encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])  
        
        # check for existing email address
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400
        
        if db.users.insert_one(user):
            return self.start_session(user)
        
        return jsonify({"error": "Signup failed"}), 400
    
    def signout(self):
        session.clear()
        return redirect('/')
    
    def login(self):
        user = db.users.find_one({
        "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        
        return jsonify({ "error": "Invalid username and password" }), 401
    
    def forgetPass(self):
        print(request.form.get('email'))
        print(1 if db.users.find_one({"email": request.form.get('email')}) else 0)
        user = db.users.find_one({"email": request.form.get('email')})
        if user:
            return self.start_session(user)
        
        return jsonify({ "error": "Email address not found" }), 401
    
    def resetPass(self):
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        #confirm password
        if new_password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 401
        
        # encrypt the password
        new_password = pbkdf2_sha256.encrypt(new_password)  
        if db.users.update_one({"email": session['user']['email']}, {"$set": {"password": new_password}}).modified_count > 0: 
            session.clear()
            return jsonify({ "success": "Password reset successful" }), 200
        
        return jsonify({ "error": "Reset password failed" }), 400
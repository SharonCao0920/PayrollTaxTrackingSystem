import secrets

from flask import Flask, redirect, request, jsonify, session, url_for, make_response
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
            "password": request.form.get('password'),
            "reset_token": None
        }
        
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

    def forget_password(self):
        email = request.form.get('email')
        user = db.users.find_one({"email": email})
        if user:
            return jsonify({"message": "Reset password email has been sent."}), 200
            # reset_token = secrets.token_urlsafe(16)
            # db.users.update_one({"email": email}, {"$set": {"reset_token": reset_token}})
            # reset_link = url_for('reset_password', token=reset_token, _external=True)
            # User().send_reset_email(email, reset_link)
            # response = make_response(jsonify({"message": "Reset password email has been sent."}), 200)
        else:
            return jsonify({"error": "Email address not found."}), 404

    def reset_password(self):
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        if new_password == confirm_password:
            return jsonify({"message": "Password reset successfully."}), 200
        else:
            return jsonify({"error": "Passwords do not match."}), 400
        # user = db.users.find_one({"reset_token": token})
        # if user:
        #     hashed_password = pbkdf2_sha256.encrypt(new_password)
        #     db.users.update_one({"reset_token": token}, {"$set": {"password": hashed_password}})
        #     db.users.update_one({"reset_token": token}, {"$unset": {"reset_token": ""}})
        #     return "Password reset successfully."
        # else:
        #     return "Invalid reset token."

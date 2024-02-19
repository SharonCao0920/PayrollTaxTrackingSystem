import glob
import secrets
import shutil

import groupdocs_comparison_cloud
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
    def comparePdf(self):
        client_id = "c7c24845-f54f-45c1-aead-d0e876e5c217"
        client_secret = "6e8433eaf16891494e63d1bb95740431"

        configuration = groupdocs_comparison_cloud.Configuration(client_id, client_secret)
        configuration.api_base_url = "https://api.groupdocs.cloud"
        my_storage = ""
        # This code example demonstrates how to upload PDF files to the cloud.
        # Create instance of the API
        file_api = groupdocs_comparison_cloud.FileApi.from_config(configuration)

        # upload sample files
        for filename in glob.iglob("C:\\Files\\*.pdf", recursive=True):
            destFile = filename.replace("C:\\Files\\", "", 1)
        file_api.upload_file(groupdocs_comparison_cloud.UploadFileRequest(destFile, filename))
        print("Uploaded file: " + destFile)
        # This code example demonstrates how to compare two PDF files.
        # Create an instance of the API
        api_instance = groupdocs_comparison_cloud.CompareApi.from_keys(client_id, client_secret)

        # Input source file
        source = groupdocs_comparison_cloud.FileInfo()
        source.file_path = "source.pdf"

        # Target file
        target = groupdocs_comparison_cloud.FileInfo()
        target.file_path = "target.pdf"

        # Define comparison options
        options = groupdocs_comparison_cloud.ComparisonOptions()
        options.source_file = source
        options.target_files = [target]
        options.output_path = "result.pdf"

        # Create comparison request
        request = groupdocs_comparison_cloud.ComparisonsRequest(options)

        # compare
        response = api_instance.comparisons(request)

        # This code example demonstrates how to download the resulting file.
        # Create instance of the API
        file_api = groupdocs_comparison_cloud.FileApi.from_config(configuration)

        # Create download file request
        request = groupdocs_comparison_cloud.DownloadFileRequest("result.pdf", my_storage)

        # Download file
        response = file_api.download_file(request)

        # Move downloaded file to your working directory
        shutil.move(response, "C:\\Files\\")
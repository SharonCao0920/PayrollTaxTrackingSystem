import glob
import shutil

import groupdocs_comparison_cloud
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

        # create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        # confirm password
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

        return jsonify({"error": "Invalid username and password"}), 401

    def forgetPass(self):
        print(request.form.get('email'))
        print(1 if db.users.find_one({"email": request.form.get('email')}) else 0)
        user = db.users.find_one({"email": request.form.get('email')})
        if user:
            return self.start_session(user)

        return jsonify({"error": "Email address not found"}), 401

    def resetPass(self):
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        # confirm password
        if new_password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 401

        # encrypt the password
        new_password = pbkdf2_sha256.encrypt(new_password)
        if db.users.update_one({"email": session['user']['email']},
                               {"$set": {"password": new_password}}).modified_count > 0:
            session.clear()
            return jsonify({"success": "Password reset successful"}), 200

        return jsonify({"error": "Reset password failed"}), 400

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

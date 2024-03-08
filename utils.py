import glob
import secrets
import shutil

import groupdocs_comparison_cloud
from flask import Flask, redirect, request, jsonify, session, url_for, make_response
from passlib.hash import pbkdf2_sha256

from app import db
import uuid

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
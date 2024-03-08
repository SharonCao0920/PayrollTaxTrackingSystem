from datetime import datetime
from flask import jsonify, request
from app import app, otp_collection
from generateOTP.models import generate_otp, send_otp_by_email, verify_otp

# API endpoint to generate and send OTP
@app.route('/generateOTP/generate-otp/', methods=['POST'])
def generate_otp_endpoint():
    data = request.json
    email = data.get('email')
    otp = generate_otp()

    otp_collection.insert_one({"email": email, "otp": otp, "timestamp": datetime.now()})
    send_otp_by_email(email, otp)

    return jsonify({"success": True})


# Verify OTP Endpoint
@app.route('/generateOTP/verify-otp/', methods=['POST'])
def verify_otp_endpoint():
    data = request.json
    otp = data.get('otp')
    verification_result = verify_otp(otp)

    return jsonify({"status": verification_result})
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import random
import smtplib
from app import otp_collection

# mail transporter setup... replace setup with project mail setup
smtp_host = os.getenv("smtp_host")
smtp_port = os.getenv("smtp_port")
smtp_user = os.getenv("smtp_user")
smtp_pass = os.getenv("smtp_pass")

# Generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))


# Send OTP via email
def send_otp_by_email(email, otp):
    msg = MIMEMultipart()
    msg['From'] = 'ennydiamond@yahoo.com' #replace mail with project mail 
    msg['To'] = email
    msg['Subject'] = 'OTP for Verification'
    body = f'Your OTP is: {otp}'
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, email, msg.as_string())
    print('OTP sent to', email)


# Verify OTP
def verify_otp(otp):
    otp_data = otp_collection.find_one({"otp": otp})
    if not otp_data:
        return "not found"

    timestamp = otp_data["timestamp"]
    current_time = datetime.now()
    difference_in_minutes = (current_time - timestamp).total_seconds() / 60

    if difference_in_minutes > 5:
        return "expired"

    return "ok"
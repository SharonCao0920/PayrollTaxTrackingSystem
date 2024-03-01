from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps
import random
import smtplib
from flask import Flask, jsonify, redirect, render_template, request, session
import pymongo
from dotenv import load_dotenv
import os

from werkzeug import Client




app = Flask(__name__)  
app.secret_key = "secret"

#test
load_dotenv()
URI = os.getenv("DATABASE_URI")
#client = pymongo.MongoClient(URI)
#db = Client.get_database("user_login_system")


#database
client = pymongo.MongoClient(URI)
db = client.user_login_system

otp_collection = db.otp_collection



# mail transporter setup... replace setup with project mail setup
smtp_host = 'smtp.mail.yahoo.com'
smtp_port = 465
smtp_user = 'ennydiamond@yahoo.com'
smtp_pass = 'cuojgnjurjsllgal'



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

@app.route('/generate/')
def generate():
    return render_template('generateOTP.html')


@app.route('/calculate/')
def calculate():
    return render_template('calculateTax.html')



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

def calculate_federal_taxes(gross_income, filing_status):
    # Constants for Federal Taxes
    FUTA_RATE = 0.006
    SSA_RATE = 0.062
    FUTA_CAP = 7000
    SSA_CAP = 137700
    federal_tax_rate = 0.22 if filing_status == 'single' else 0.24

    federal_tax = gross_income * federal_tax_rate
    futa_tax = min(gross_income, FUTA_CAP) * FUTA_RATE
    ssa_tax = min(gross_income, SSA_CAP) * SSA_RATE

    return {
        'federal_tax': round(federal_tax, 2),
        'futa_tax': round(futa_tax, 2),
        'ssa_tax': round(ssa_tax, 2)
    }

def calculate_ca_taxes(gross_income):
    # Constants for California State Taxes
    CA_STATE_TAX_RATE = 0.08  # Simplified average rate
    CA_SDI_RATE = 0.01  # State Disability Insurance rate
    CA_SDI_CAP = 122909  # Adjust as necessary

    ca_state_tax = gross_income * CA_STATE_TAX_RATE
    ca_sdi_tax = min(gross_income, CA_SDI_CAP) * CA_SDI_RATE

    return {
        'ca_state_tax': round(ca_state_tax, 2),
        'ca_sdi_tax': round(ca_sdi_tax, 2)
    }


# API endpoint to generate and send OTP
@app.route('/generate-otp', methods=['POST'])
def generate_otp_endpoint():
    data = request.json
    email = data.get('email')
    otp = generate_otp()

    otp_collection.insert_one({"email": email, "otp": otp, "timestamp": datetime.now()})
    send_otp_by_email(email, otp)

    return jsonify({"success": True})


# Verify OTP Endpoint
@app.route('/verify-otp', methods=['POST'])
def verify_otp_endpoint():
    data = request.json
    otp = data.get('otp')
    verification_result = verify_otp(otp)

    return jsonify({"status": verification_result})
       
@app.route('/calculatetax', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        gross_income = float(request.form['gross_income'])
        filing_status = request.form['filing_status']
        
        federal_taxes = calculate_federal_taxes(gross_income, filing_status)
        ca_taxes = calculate_ca_taxes(gross_income)
        
        total_taxes = sum(federal_taxes.values()) + sum(ca_taxes.values())

        return render_template('taxResult.html', federal_taxes=federal_taxes, ca_taxes=ca_taxes, total_taxes=round(total_taxes, 2))
    return render_template('taxResult.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import render_template, request
from app import app
from calculateTax.models import calculate_ca_taxes, calculate_federal_taxes



@app.route('/calculateTax/calculatetax', methods=['POST'])
def index():
    gross_income = float(request.form['gross_income'])
    filing_status = request.form['filing_status']
        
    federal_taxes = calculate_federal_taxes(gross_income, filing_status)
    ca_taxes = calculate_ca_taxes(gross_income)
        
    total_taxes = sum(federal_taxes.values()) + sum(ca_taxes.values())

    return render_template('taxResult.html', federal_taxes=federal_taxes, ca_taxes=ca_taxes, total_taxes=round(total_taxes, 2))

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
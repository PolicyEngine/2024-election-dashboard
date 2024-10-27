# Colors
BLUE = "#3378b2"
RED = "#f45959"
GREY = "#868686"

# State Codes and Names
STATE_NAMES = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DC": "District of Columbia",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}

STATE_CODES = list(STATE_NAMES.keys())

# Simulation constants
YEAR = "2025"
DEFAULT_AGE = 40

# In utils.py
BASE_YEAR = 2024  # Year for input values
AVAILABLE_YEARS = [2025, 2026, 2027, 2028]  # Years for results


# Main metrics that are always shown
MAIN_METRICS = [
    "Household Net Income",
    "Income Tax Before Credits",
    "Refundable Tax Credits",
]

# Acronyms for credit formatting
CREDIT_ACRONYMS = {"eitc": "EITC", "ctc": "CTC"}


def format_credit_name(name, state_code=None):
    """Format credit names to be more readable"""
    # Remove tax_unit prefix if present
    name = name.replace("tax_unit_", "")

    # Handle state-specific credits
    if "state_name" in name.lower() and state_code:
        state_name = STATE_NAMES.get(state_code, state_code)
        name = name.replace("state_name", state_name)

    # Replace underscores with spaces and capitalize each word
    formatted = name.replace("_", " ").title()

    # Replace any lowercase acronyms with uppercase versions
    for acronym_lower, acronym_upper in CREDIT_ACRONYMS.items():
        formatted = formatted.replace(acronym_lower.title(), acronym_upper)

    return formatted


def format_currency(value):
    """Format a number as currency string"""
    return f"${value:,.2f}"

def calculate_uprated_value(base_value, base_year, target_year, annual_rate=0.03):
    """
    Calculate the uprated value based on a 3% annual increase
    
    Args:
        base_value: Original value in base year dollars
        base_year: Year the value is originally in (int)
        target_year: Year to project the value to (int)
        annual_rate: Annual uprating rate (default 0.03 for 3%)
    """
    years_difference = target_year - base_year
    if years_difference <= 0:
        return base_value
    return base_value * ((1 + annual_rate) ** years_difference)

def uprate_inputs(inputs, base_year, target_year):
    """
    Uprate all monetary inputs from base year to target year
    """
    monetary_fields = [
        'income', 'spouse_income', 'social_security', 'capital_gains',
        'medical_expenses', 'real_estate_taxes', 'interest_expense',
        'charitable_cash', 'charitable_non_cash', 'qualified_business_income',
        'casualty_loss'
    ]
    
    uprated_inputs = inputs.copy()
    for field in monetary_fields:
        if field in inputs:
            uprated_inputs[field] = calculate_uprated_value(
                inputs[field], 
                base_year, 
                target_year
            )
    
    return uprated_inputs
# Colors
BLUE = "#3378b2"
RED = "#f45959"
GREY = "#868686"

# Tariff rates
CHINA_TARIFF_RATE = 0.60  # 60% tariff on Chinese imports
OTHER_TARIFF_RATE = 0.10  # 10% tariff on other imports


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
    "NYC": "New York City",
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

STATE_CREDIT_MAP = {
    "CA": ["ca_yctc", "ca_eitc"],
    "CO": ["co_ctc", "co_eitc"],
    "CT": [None, "ct_eitc"],
    "DC": [None, "dc_eitc"],
    "DE": [None, "de_eitc"],
    "HI": [None, "hi_eitc"],
    "IA": [None, "ia_eitc"],
    "IL": [None, "il_eitc"],
    "IN": [None, "in_eitc"],
    "KS": [None, "ks_total_eitc"],
    "LA": [None, "la_eitc"],
    "MA": [None, "ma_eitc"],
    "MD": ["md_ctc", "md_eitc"],
    "ME": [None, "me_eitc"],
    "MI": [None, "mi_eitc"],
    "MN": ["mn_child_and_working_families_credits", None],
    "MO": [None, "mo_wftc"],
    "MT": ["mt_ctc", "mt_eitc"],
    "NC": ["nc_ctc", None],
    "NE": [None, "ne_eitc"],
    "NJ": ["nj_ctc", "nj_eitc"],
    "NM": ["nm_ctc", "nm_eitc"],
    "NY": ["ny_ctc", "ny_eitc"],
    "OH": [None, "oh_eitc"],
    "OK": [None, "ok_eitc"],
    "OR": ["or_ctc", "or_eitc"],
    "RI": [None, "ri_eitc"],
    "SC": [None, "sc_eitc"],
    "UT": [None, "ut_eitc"],
    "VA": [None, "va_eitc"],
    "VT": ["vt_ctc", "vt_eitc"],
    "WA": [None, "wa_working_families_tax_credit"],
    "WI": [None, "wi_earned_income_credit"],
}

STATE_CODES = list(STATE_NAMES.keys())

# Simulation constants
YEAR = "2025"
DEFAULT_AGE = 40

# Main metrics that are always shown
MAIN_METRICS = [
    "Household Net Income",
    "Household Market Income",
    "Income Tax Before Credits",
    "Federal Refundable Credits",
    "State Refundable Credits",
    "Total Benefits",
]

# Acronyms for credit formatting
CREDIT_ACRONYMS = {"eitc": "EITC", "ctc": "CTC"}


def format_credit_name(name, state_code=None):
    """Format credit names to be more readable"""
    # Remove tax_unit prefix if present
    name = name.replace("tax_unit_", "")

    # Handle state-specific credits
    if "state_name" in name.lower() and state_code:
        # Handle NYC specially
        if state_code == "NY" and "nyc" in name.lower():
            state_name = STATE_NAMES["NYC"]
        else:
            state_name = STATE_NAMES.get(state_code, state_code)
        name = name.replace("state_name", state_name)

    # Replace underscores with spaces and capitalize each word
    formatted = name.replace("_", " ").title()

    # Replace any lowercase acronyms with uppercase versions
    for acronym_lower, acronym_upper in CREDIT_ACRONYMS.items():
        formatted = formatted.replace(acronym_lower.title(), acronym_upper)

    return formatted


def format_currency(value):
    """Format a number as currency without decimal places"""
    return f"${int(round(value)):,}"


def format_program_name(name):
    """Format program names to be more readable"""
    return name.replace("_", " ").title()

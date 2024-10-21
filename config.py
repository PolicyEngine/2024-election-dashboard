from utils import GRAY, BLUE, LIGHT_RED, LIGHTER_RED

REFORMS = {
    "Baseline": {
        "name": "Baseline",
        "color": GRAY,
        "description": "The current tax system without any proposed changes.",
        "link": "https://policyengine.org/us/policy"
    },
    "Harris LIFT Middle Class Tax Credit": {
        "name": "Harris LIFT Middle Class Tax Credit",
        "color": BLUE,
        "description": "A tax credit proposed by Vice President Kamala Harris to provide additional support for middle-class families.",
        "link": "https://policyengine.org/us/research/lift-act"
    },
    "Harris Rent Relief Act": {
        "name": "Harris Rent Relief Act",
        "color": BLUE,
        "description": "A proposal by Vice President Kamala Harris to provide tax credits for renters to alleviate housing costs.",
        "link": "https://policyengine.org/us/research/rent-relief-act"
    },
    "Vance Child Tax Credit (refundable version)": {
        "name": "Vance Child Tax Credit (non-refundable version)",
        "color": LIGHTER_RED,
        "description": "Senator JD Vance's suggestion to expand the Child Tax Credit to $5,000, modeled as non-refundable.",
        "link": "https://policyengine.org/us/research/vance-ctc"
    },
    "Vance Child Tax Credit (non-refundable version)": {
        "name": "Vance Child Tax Credit (refundable version)",
        "color": LIGHT_RED,
        "description": "Senator JD Vance's suggestion to expand the Child Tax Credit to $5,000, modeled as fully refundable.",
        "link": "https://policyengine.org/us/research/vance-ctc"
    },
    "Harris Child Tax Credit": {
        "name": "Harris Child Tax Credit",
        "color": BLUE,
        "description": "Vice President Kamala Harris's proposal to expand the Child Tax Credit, including a 'baby bonus' and increased credit amounts.",
        "link": "https://policyengine.org/us/research/harris-ctc"
    },
    "Harris High Earners Reform": {
        "name": "Harris High Earners Reform",
        "color": BLUE,
        "description": "A proposal by Vice President Kamala Harris to adjust tax rates and thresholds for high-income earners."
    },
    "Trump Social Security": {
        "name": "Trump Social Security Tax Exemption",
        "color": LIGHT_RED,
        "description": "A proposal to exempt Social Security benefits from taxation, as suggested by former President Donald Trump.",
        "link": "https://policyengine.org/us/research/social-security-tax-exemption"
    },
    "Harris Restoring ARPA EITC": {
        "name": "Harris Restoring ARPA EITC",
        "color": BLUE,
        "description": "Vice President Kamala Harris's proposal to restore and expand the Earned Income Tax Credit (EITC) to ARPA levels."    
    }
}

APP_TITLE = "2024 Election, Personal Household Impact Calculator"

BASELINE_DESCRIPTION = """
## Current Tax System
This calculator compares various proposed tax reforms to the current (baseline) tax system. 
Enter your household information below to see how these reforms might affect your net income.
[Learn more about the current US tax system](https://policyengine.org/us/policy)
"""

REFORMS_DESCRIPTION = """
Several reforms have been proposed by candidates and policymakers for the 2024 election:

- **Harris LIFT Middle Class Tax Credit**: Vice President Kamala Harris has proposed the LIFT (Livable Incomes for Families Today) Act to provide additional support for middle-class families.
  [Read our full report on the LIFT Act.](https://policyengine.org/us/research/lift-act)

- **Harris Rent Relief Act**: This proposal by Vice President Kamala Harris aims to provide tax credits for renters to alleviate housing costs.
  [Read our full report on the Rent Relief Act.](https://policyengine.org/us/research/rent-relief-act)

- **Harris Child Tax Credit**: The Harris-Walz economic plan calls for restoring the 2021 expansion of the Child Tax Credit, making it fully refundable and more generous, and adding a $2,400 "baby bonus".
  [Read our full report on the Harris-Walz CTC proposal.](https://policyengine.org/us/research/harris-ctc)

- **Vance Child Tax Credit Proposals**: In an August 2024 interview, Senator and Vice Presidential nominee JD Vance suggested expanding the Child Tax Credit to $5,000. Vance did not specify whether it was refundable, so we modeled both refundable and non-refundable scenarios.
  [Read our full report on JD Vance's suggested CTC expansion.](https://policyengine.org/us/research/vance-ctc)

- **Trump Social Security Tax Exemption**: Former President Donald Trump has proposed exempting Social Security benefits from taxation.
  [Read our full report on the Social Security tax exemption proposal.](https://policyengine.org/us/research/social-security-tax-exemption)

- **Harris High Earners Reform**: Vice President Kamala Harris has proposed adjusting tax rates and thresholds for high-income earners. (Detailed analysis coming soon)

- **Harris Restoring ARPA EITC**: Vice President Kamala Harris has proposed restoring the American Rescua Plan Version of the Earned Income Tax Credit. (Detailed analysis coming soon)

"""

NOTES = """
### Assumptions and Notes:
- All calculations are based on projected 2025 tax parameters.
- The calculator assumes all income is from employment (wages and salaries).
- It uses standard deductions and does not account for itemized deductions.
- State and local taxes are not considered in this federal-level analysis.
- The calculator uses the PolicyEngine US microsimulation model.
- Actual impacts may vary based on individual circumstances and final policy implementations.
"""
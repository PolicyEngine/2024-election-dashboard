from utils import GRAY, BLUE, LIGHT_RED

APP_TITLE = "2024 Election, Personal Household Impact Calculator"

BASELINE_DESCRIPTION = """
## Current Tax System
This calculator compares various proposed tax reforms to the current (baseline) tax system. 
Enter your household information below to see how these reforms might affect your net income.
[Learn more about the current US tax system](https://policyengine.org/us/policy)
"""

REFORMS_DESCRIPTION = """
This calculator compares the economic proposals of the two major party tickets in the 2024 presidential election:

### Harris-Walz Economic Package
The Harris-Walz platform includes several major tax reforms:
- **LIFT Middle Class Tax Credit**: Additional support for middle-class families through tax credits
  [Learn more about the LIFT Act](https://policyengine.org/us/research/lift-act)
- **Rent Relief Act**: Tax credits for renters to alleviate housing costs
  [Learn more about the Rent Relief Act](https://policyengine.org/us/research/rent-relief-act)
- **Enhanced Child Tax Credit**: Restoring the 2021 expansion with full refundability and a $2,400 "baby bonus"
  [Learn more about the Harris CTC](https://policyengine.org/us/research/harris-ctc)
- **High Earners Reform**: Adjustments to tax rates and thresholds for high-income earners
- **Restored EITC**: Bringing back the expanded American Rescue Plan version of the Earned Income Tax Credit

### Trump-Vance Economic Package
The Trump-Vance platform includes:
- **Social Security Tax Exemption**: Eliminating taxes on Social Security benefits
  [Learn more about the Social Security proposal](https://policyengine.org/us/research/social-security-tax-exemption)
- **$5,000 Child Tax Credit**: An expanded, fully refundable Child Tax Credit
  [Learn more about the Vance CTC](https://policyengine.org/us/research/vance-ctc)
"""

NOTES = """
### Assumptions and Notes:
- All calculations are based on projected 2025 tax parameters.
- The calculator assumes all income is from employment (wages and salaries).
- It uses standard deductions and does not account for itemized deductions.
- State and local taxes are not considered in this federal-level analysis.
- The calculator uses the PolicyEngine US microsimulation model.
- Actual impacts may vary based on individual circumstances and final policy implementations.
- Proposals are modeled based on currently available information and may be updated as more details are released.
"""
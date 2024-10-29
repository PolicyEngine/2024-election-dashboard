APP_TITLE = "2024 Election, Personal Household Impact Calculator"

BASELINE_DESCRIPTION = """
This calculator compares how tax proposals from the two major party presidential candidates would affect your household's net income. Enter your household information below to see a personalized analysis of each plan's impact.

**Learn More:**
- [Harris Economic Policy Document](https://kamalaharris.com/wp-content/uploads/2024/09/Policy_Book_Economic-Opportunity.pdf)
- [Trump Campaign Platform](https://rncplatform.donaldjtrump.com/?_gl=1*s9hec5*_gcl_au*MTE5NjQwNTg0MC4xNzI3ODgwOTQw&_ga=2.140186549.721558943.1727880940-379257754.1727880940)
"""

REFORMS_DESCRIPTION = """
This calculator compares the economic proposals of the two major party tickets in the 2024 presidential election:

### Harris Economic Package
The Harris platform includes several major tax reforms:
- **Enhanced Child Tax Credit**: Restoring the 2021 expansion with full refundability and a $2,400 "baby bonus"
  [Read our full report on the Harris CTC proposal](https://policyengine.org/us/research/harris-ctc)
- **High Earners Reform**: High earners face a 39.6% tax rate on income above \$418,450 (single) or \$462,400 (married), plus increased Medicare and Net Investment Income tax of 1.2% on income above \$411,000
- **Restored EITC**: Bringing back the expanded American Rescue Plan version of the Earned Income Tax Credit
  [Read our full report on the Harris EITC proposal](https://policyengine.org/us/research/harris-eitc)
- **Tip Income Tax Relief**: Exempting tip income from income tax but not payroll taxes
- **Capital Gains Reform**: Creating a new 28% tax bracket for capital gains income over $1,000,000

### Trump Economic Package
The Trump platform includes:
- **Social Security Tax Exemption**: Eliminating taxes on Social Security benefits for senior citizens 
  [Read our full report on the Trump Social Security proposal](https://policyengine.org/us/research/social-security-tax-exemption)
- **Tip Income Tax Relief**: Exempting all tip income from both income and payroll taxes
- **Overtime Tax Relief**: Exempting all overtime income from both income and payroll taxes
- **Import Tariffs**: Implementing a 60% tariff on imported goods from China and a 10% tariff on imported goods from all other countries


"""

NOTES = """
### Assumptions and Notes:
- All calculations are based on projected 2025 tax parameters.
- The calculator assumes all income is from employment (wages and salaries).
- Whether to use standard or itemized deductions is calculated based on the user input.
- The calculator uses the PolicyEngine US microsimulation model.
- Actual impacts may vary based on individual circumstances and final policy implementations.
- Proposals are modeled based on currently available information and may be updated as more details are released.
- Tax exemptions for tip and overtime income apply to both income tax and payroll taxes under the specified reforms.
- We assume that tariffs are fully passed through to consumers in the form of higher prices
- The modeled tariff rates (60% for China, 10% for other countries) are applied on top of any existing tariff rates.
- We include a simplified model of tariff impacts and actual effects may vary based on market conditions and business responses.
"""

ADDITIONAL_POLICIES = """
### Additional Tax & Benefit Proposals Not Currently Modeled

#### Harris Additional Tax Proposals
- **TCJA Extension**
  - Extend 2017 tax law provisions selectively based on income:
    * Full extension for households earning less than $400,000
    * Limited benefits for households earning above $400,000
  - Note: This calculator shows 2025 impacts only, before TCJA provisions expire

 - **Healthcare Cost Caps**
    - Extend Medicare's prescription drug cost limits to all Americans:
    * $35 monthly cap on insulin costs
    * $2,000 annual cap on out-of-pocket prescription costs 

- **Housing Tax Credits**
  - Expanding the low-income housing tax credit
  - Creating new credits for homebuilding in low-income communities

- **Business Support**
  - Increase startup expense deduction from \$5,000 to \$50,000
  - Simplify tax filing process for small businesses
  - New "America Forward tax credit" for strategic industry investment

- **Corporate Tax Changes**
  - Raise corporate tax rate from 21% to 28%
  - Increase stock buyback excise tax from 1% to 4%

#### Trump Additional Tax Proposals
- **TCJA Extension**
  - Proposed extension of the Tax Cuts and Jobs Act provisions set to expire in 2026
  - Note: This calculator shows 2025 impacts only, before TCJA provisions expire
  - [Read our full report on the TCJA extension](https://policyengine.org/us/research/tcja-extension)

- **Business Tax Changes**
  - Make Tax Cuts and Jobs Act (TCJA) business provisions more generous
  - Expand business tax breaks

- **Energy Policy**
  - Rescind unspent clean energy tax incentives from Inflation Reduction Act
  - Roll back green energy tax breaks

- **Corporate Tax Rate**
  - Cut corporate tax rate from 21% to 15% for domestic production

*Note: These additional policies are not currently modeled in the calculator but represent stated policy positions from both campaigns.*
"""

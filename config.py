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
  [Learn more about the Harris CTC](https://policyengine.org/us/research/harris-ctc)
- **High Earners Reform**: High earners face a 39.6% tax rate on income above $418,450 (single) or $462,400 (married), plus increased Medicare and Net Investment Income tax of 1.2% on income above $411,000
- **Restored EITC**: Bringing back the expanded American Rescue Plan version of the Earned Income Tax Credit
- **Tip Income Tax Relief**: Exempting tip income from both income and payroll taxes

  [Learn more about the Harris EITC proposal](https://policyengine.org/us/research/harris-eitc)
- **Capital Gains Reform**: Creating a new 28% tax bracket for capital gains income over $1,000,000

### Trump Economic Package
The Trump platform includes:
- **Social Security Tax Exemption**: Eliminating taxes on Social Security benefits for senior citizens 
  [Learn more about the Social Security proposal](https://policyengine.org/us/research/social-security-tax-exemption)
- **Tip Income Tax Relief**: Exempting all tip income from both income and payroll taxes
- **Overtime Tax Relief**: Exempting all overtime income from both income and payroll taxes
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
"""

ADDITIONAL_POLICIES = """
### Additional Tax & Benefit Proposals Not Currently Modeled

#### Harris Additional Tax Proposals
- **Housing Tax Credits**
  - Expanding the low-income housing tax credit
  - Creating new credits for homebuilding in low-income communities
  - Supporting affordable housing development

- **Business Support**
  - Increase startup expense deduction from $5,000 to $50,000
  - Simplify tax filing process for small businesses
  - New "America Forward tax credit" for strategic industry investment

- **Corporate Tax Changes**
  - Raise corporate tax rate from 21% to 28%
  - Increase stock buyback excise tax from 1% to 4%

#### Trump Additional Tax Proposals
- **Business Tax Changes**
  - Make Tax Cuts and Jobs Act (TCJA) business provisions more generous
  - Expand business tax breaks
  - Focus on domestic production incentives

- **Energy Policy**
  - Rescind unspent clean energy tax incentives from Inflation Reduction Act
  - Roll back green energy tax breaks

- **Corporate Tax Rate**
  - Cut corporate tax rate from 21% to 15% for domestic production
  - Focus on encouraging domestic manufacturing

- **Import Tariffs**
  - 10% tariff on all imports
  - 60% tariffs on imports from China

*Note: These additional policies are not currently modeled in the calculator but represent stated policy positions from both campaigns.*
"""
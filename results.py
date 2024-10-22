from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from reforms import COMBINED_REFORMS  # Updated import
from utils import YEAR, DEFAULT_AGE

def create_situation(state, is_married, child_ages, income, rent, fair_market_rent, social_security_retirement):
    situation = {
        "people": {
            "adult": {
                "age": {YEAR: DEFAULT_AGE},
                "employment_income": {YEAR: income},
                "rent": {YEAR: rent},
                "social_security_retirement": {YEAR: social_security_retirement},
            },
        },
        "families": {"family": {"members": ["adult"]}},
        "marital_units": {"marital_unit": {"members": ["adult"]}},
        "tax_units": {
            "tax_unit": {
                "members": ["adult"],
                # Performance improvement settings
                "premium_tax_credit": {YEAR: 0},
                "tax_unit_itemizes": {YEAR: False},
                "taxable_income_deductions_if_itemizing": {YEAR: 0},
                "alternative_minimum_tax": {YEAR: 0},
                "net_investment_income_tax": {YEAR: 0},
            }
        },
        "households": {
            "household": {
                "members": ["adult"], 
                "state_code": {YEAR: state},
                "small_area_fair_market_rent": {YEAR: fair_market_rent} 
            }
        },
        "spm_units": {"household": {"members": ["adult"]}},
    }

    for i, age in enumerate(child_ages):
        child_id = f"child_{i}"
        situation["people"][child_id] = {"age": {YEAR: age}}
        for unit in ["families", "tax_units", "households", "spm_units"]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append(child_id)

    if is_married:
        situation["people"]["spouse"] = {
            "age": {YEAR: DEFAULT_AGE},
        }
        for unit in ["families", "marital_units", "tax_units", "households", "spm_units"]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append("spouse")

    return situation

def calculate_results(selected_reforms, state, is_married, child_ages, income, rent, fair_market_rent, social_security_retirement):
    results = {}
    situation = create_situation(state, is_married, child_ages, income, rent, fair_market_rent, social_security_retirement)

    # Calculate baseline
    baseline_simulation = Simulation(situation=situation)
    results["Baseline"] = baseline_simulation.calculate("household_net_income", YEAR)[0]

    # Calculate selected reforms
    for reform_name in selected_reforms:
        reform_dict = COMBINED_REFORMS.get(reform_name, {})
        if reform_dict:  # Skip if None (baseline)
            reform = Reform.from_dict(reform_dict, country_id="us")
            simulation = Simulation(reform=reform, situation=situation)
            results[reform_name] = simulation.calculate("household_net_income", YEAR)[0]

    return results
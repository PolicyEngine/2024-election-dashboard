from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from reforms import COMBINED_REFORMS
from utils import YEAR, DEFAULT_AGE
import pandas as pd

def create_situation(state, is_married, child_ages, income, social_security_retirement,
                    head_age, spouse_age=None, medical_expenses=0, real_estate_taxes=0,
                    interest_expense=0, charitable_cash=0, charitable_non_cash=0,
                    qualified_business_income=0, casualty_loss=0):
    situation = {
        "people": {
            "adult": {
                "age": {YEAR: head_age},
                "employment_income": {YEAR: income},
                "social_security_retirement": {YEAR: social_security_retirement},
                "medical_out_of_pocket_expenses": {YEAR: medical_expenses},
                "interest_expense": {YEAR: interest_expense},
                "charitable_cash_donations": {YEAR: charitable_cash},
                "charitable_non_cash_donations": {YEAR: charitable_non_cash},
                "qualified_business_income": {YEAR: qualified_business_income},
                "casualty_loss": {YEAR: casualty_loss},
                "real_estate_taxes": {YEAR: real_estate_taxes},
            },
        },
        "families": {"family": {"members": ["adult"]}},
        "marital_units": {"marital_unit": {"members": ["adult"]}},
        "tax_units": {
            "tax_unit": {
                "members": ["adult"],
                # Performance improvement settings
                "premium_tax_credit": {YEAR: 0},
                "alternative_minimum_tax": {YEAR: 0},
                "net_investment_income_tax": {YEAR: 0},
            }
        },
        "households": {
            "household": {
                "members": ["adult"], 
                "state_code": {YEAR: state},
            }
        },
        "spm_units": {"household": {"members": ["adult"]}},
    }

    for i, age in enumerate(child_ages):
        child_id = f"child_{i}"
        situation["people"][child_id] = {"age": {YEAR: age}}
        for unit in ["families", "tax_units", "households", "spm_units"]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append(child_id)

    if is_married and spouse_age is not None:
        situation["people"]["spouse"] = {
            "age": {YEAR: spouse_age},
        }
        for unit in ["families", "marital_units", "tax_units", "households", "spm_units"]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append("spouse")

    return situation

def calculate_results(selected_reforms, state, is_married, child_ages, income, social_security_retirement,
                     head_age, spouse_age=None, medical_expenses=0, real_estate_taxes=0, 
                     interest_expense=0, charitable_cash=0, charitable_non_cash=0, 
                     qualified_business_income=0, casualty_loss=0):
    results = {}
    situation = create_situation(
        state, is_married, child_ages, income, social_security_retirement,
        head_age, spouse_age, medical_expenses, real_estate_taxes, interest_expense,
        charitable_cash, charitable_non_cash, qualified_business_income,
        casualty_loss
    )

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

def calculate_detailed_metrics(state, is_married, child_ages, income, social_security_retirement,
                             head_age, spouse_age=None, medical_expenses=0, real_estate_taxes=0,
                             interest_expense=0, charitable_cash=0, charitable_non_cash=0,
                             qualified_business_income=0, casualty_loss=0):
    """Calculate detailed tax metrics for all reforms after the bar chart is displayed"""
    situation = create_situation(
        state, is_married, child_ages, income, social_security_retirement,
        head_age, spouse_age, medical_expenses, real_estate_taxes, interest_expense,
        charitable_cash, charitable_non_cash, qualified_business_income,
        casualty_loss
    )
    
    # Initialize DataFrame with reforms as columns and metrics as rows
    columns = ["Baseline", "Harris-Walz", "Trump-Vance"]
    rows = [
        "Household Net Income",
        "Income Tax Before Credits",
        "Refundable Tax Credits"
    ]
    
    detailed_df = pd.DataFrame(
        index=rows,
        columns=columns,
        dtype=float
    )
    
    # Map the row names to their corresponding variables
    variable_map = {
        "Household Net Income": "household_net_income",
        "Income Tax Before Credits": "income_tax_before_refundable_credits",
        "Refundable Tax Credits": "income_tax_refundable_credits"
    }

    # Calculate for each reform
    for reform_name in columns:
        if reform_name == "Baseline":
            simulation = Simulation(situation=situation)
        else:
            reform_dict = COMBINED_REFORMS.get(reform_name, {})
            reform = Reform.from_dict(reform_dict, country_id="us")
            simulation = Simulation(reform=reform, situation=situation)
        
        # Calculate all metrics for this reform
        for row in rows:
            variable = variable_map[row]
            detailed_df.at[row, reform_name] = simulation.calculate(variable, YEAR)[0]

    return detailed_df
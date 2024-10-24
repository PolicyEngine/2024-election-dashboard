from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from reforms import COMBINED_REFORMS
from utils import YEAR
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

def calculate_consolidated_results(reform_name, state, is_married, child_ages, income, social_security_retirement,
                                head_age, spouse_age=None, medical_expenses=0, real_estate_taxes=0,
                                interest_expense=0, charitable_cash=0, charitable_non_cash=0,
                                qualified_business_income=0, casualty_loss=0):
    """
    Calculates metrics for a single reform.
    Returns a DataFrame containing all metrics for the specified reform.
    """
    # Create situation dictionary
    situation = create_situation(
        state, is_married, child_ages, income, social_security_retirement,
        head_age, spouse_age, medical_expenses, real_estate_taxes, interest_expense,
        charitable_cash, charitable_non_cash, qualified_business_income,
        casualty_loss
    )
    
    # Define all metrics we want to calculate
    metrics = {
        "Household Net Income": "household_net_income",
        "Income Tax Before Credits": "income_tax_before_refundable_credits",
        "Refundable Tax Credits": "income_tax_refundable_credits"
    }
    
    # Initialize DataFrame with just this reform
    results_df = pd.DataFrame(
        index=metrics.keys(),
        columns=["Baseline", "Harris", "Trump"],  # Keep all columns for consistency
        dtype=float
    )
    
    # Calculate metrics for just this reform
    if reform_name == "Baseline":
        simulation = Simulation(situation=situation)
    else:
        reform_dict = COMBINED_REFORMS.get(reform_name, {})
        reform = Reform.from_dict(reform_dict, country_id="us")
        simulation = Simulation(reform=reform, situation=situation)
    
    # Calculate all metrics for this reform
    for metric_name, variable in metrics.items():
        results_df.at[metric_name, reform_name] = simulation.calculate(variable, YEAR)[0]
    
    return results_df
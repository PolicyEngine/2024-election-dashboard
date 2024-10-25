from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from reforms import COMBINED_REFORMS
from policyengine_us.variables.gov.irs.credits.income_tax_refundable_credits import income_tax_refundable_credits as IncomeTaxRefundableCredits
from policyengine_us.variables.gov.states.tax.income.state_refundable_credits import state_refundable_credits as StateRefundableCredits
from utils import YEAR
import pkg_resources
import yaml
import pandas as pd

def load_credits_from_yaml(package, resource_path):
    yaml_file = pkg_resources.resource_stream(package, resource_path)
    data = yaml.safe_load(yaml_file)
    newest_year = max(data["values"].keys())
    credits = data["values"].get(newest_year, [])
    return credits

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
                "capital_gains": {YEAR: capital_gains},
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

def calculate_values(categories, simulation, year):
    result_dict = {}
    for category in categories:
        try:
            amount = simulation.calculate(category, year, map_to="household")[0]
            result_dict[category] = amount
        except:
            result_dict[category] = 0
    return result_dict

def calculate_consolidated_results(reform_name, state, is_married, child_ages, income, social_security_retirement,
                                head_age, spouse_age=None, medical_expenses=0, real_estate_taxes=0,
                                interest_expense=0, charitable_cash=0, charitable_non_cash=0,
                                qualified_business_income=0, casualty_loss=0):
    """
    Calculates metrics for a single reform with detailed breakdowns.
    """
    # Create situation dictionary
    situation = create_situation(
        state, is_married, child_ages, income, social_security_retirement,
        head_age, spouse_age, medical_expenses, real_estate_taxes, interest_expense,
        charitable_cash, charitable_non_cash, qualified_business_income,
        casualty_loss, capital_gains
    )
    
    # Set up simulation
    if reform_name == "Baseline":
        simulation = Simulation(situation=situation)
    else:
        reform_dict = COMBINED_REFORMS.get(reform_name, {})
        reform = Reform.from_dict(reform_dict, country_id="us")
        simulation = Simulation(reform=reform, situation=situation)

    # # Get categories for credits
    # federal_refundable_credits = IncomeTaxRefundableCredits.adds
    # state_refundable_credits = StateRefundableCredits.adds

    package = "policyengine_us"
    resource_path_federal = "parameters/gov/irs/credits/refundable.yaml"
    resource_path_state = f"parameters/gov/states/{state.lower()}/tax/income/credits/refundable.yaml"

    try:
        federal_refundable_credits = load_credits_from_yaml(package, resource_path_federal)
    except FileNotFoundError:
        federal_refundable_credits = []

    try:
        state_refundable_credits = load_credits_from_yaml(package, resource_path_state)
    except FileNotFoundError:
        state_refundable_credits = []


    # Calculate main metrics
    household_net_income = simulation.calculate("household_net_income", YEAR)[0]
    household_refundable_tax_credits = simulation.calculate("household_refundable_tax_credits", YEAR)[0]
    household_tax_before_refundable_credits = simulation.calculate("household_tax_before_refundable_credits", YEAR)[0]

    # Calculate credit breakdowns
    federal_credits_dict = calculate_values(federal_refundable_credits, simulation, YEAR)
    state_credits_dict = calculate_values(state_refundable_credits, simulation, YEAR)

    # Combine all results
    all_results = {
        "Household Net Income": household_net_income,
        "Income Tax Before Credits": household_tax_before_refundable_credits,
        "Refundable Tax Credits": household_refundable_tax_credits,
        **federal_credits_dict,
        **state_credits_dict
    }
    
    # Create DataFrame with all results
    results_df = pd.DataFrame(
        {reform_name: all_results}
    ).T
    
    return results_df
from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from reforms import COMBINED_REFORMS
from utils import uprate_inputs
from policyengine_us.variables.gov.irs.credits.income_tax_refundable_credits import (
    income_tax_refundable_credits as IncomeTaxRefundableCredits,
)
from policyengine_us.variables.gov.states.tax.income.state_refundable_credits import (
    state_refundable_credits as StateRefundableCredits,
)
from utils import (
    uprate_inputs,
    YEAR,
    AVAILABLE_YEARS,
    BASE_YEAR,
)
import pkg_resources
import yaml
import pandas as pd


def load_credits_from_yaml(package, resource_path):
    yaml_file = pkg_resources.resource_stream(package, resource_path)
    data = yaml.safe_load(yaml_file)
    newest_year = max(data["values"].keys())
    credits = data["values"].get(newest_year, [])
    return credits


def create_situation(
    state,
    is_married,
    child_ages,
    income,
    social_security,
    head_age,
    spouse_age=None,
    medical_expenses=0,
    real_estate_taxes=0,
    interest_expense=0,
    charitable_cash=0,
    charitable_non_cash=0,
    qualified_business_income=0,
    casualty_loss=0,
    capital_gains=0,
    spouse_income=0,
):
    situation = {
        "people": {
            "adult": {
                "age": {year_str: head_age},
                "employment_income": {year_str: income},
                "social_security": {year_str: social_security},
                "medical_out_of_pocket_expenses": {year_str: medical_expenses},
                "interest_expense": {year_str: interest_expense},
                "charitable_cash_donations": {year_str: charitable_cash},
                "charitable_non_cash_donations": {year_str: charitable_non_cash},
                "qualified_business_income": {year_str: qualified_business_income},
                "casualty_loss": {year_str: casualty_loss},
                "real_estate_taxes": {year_str: real_estate_taxes},
                "capital_gains": {year_str: capital_gains},
            },
        },
        "families": {"family": {"members": ["adult"]}},
        "marital_units": {"marital_unit": {"members": ["adult"]}},
        "tax_units": {
            "tax_unit": {
                "members": ["adult"],
                "premium_tax_credit": {year_str: 0},
                "alternative_minimum_tax": {year_str: 0},
                "net_investment_income_tax": {year_str: 0},
            }
        },
        "households": {
            "household": {
                "members": ["adult"],
                "state_code": {year_str: state},
            }
        },
        "spm_units": {"household": {"members": ["adult"]}},
    }

    for i, age in enumerate(child_ages):
        child_id = f"child_{i}"
        situation["people"][child_id] = {"age": {year_str: age}}
        for unit in ["families", "tax_units", "households", "spm_units"]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append(child_id)

    if is_married and spouse_age is not None:
        situation["people"]["spouse"] = {
            "age": {year_str: spouse_age},
            "employment_income": {year_str: spouse_income},
            "employment_income": {YEAR: spouse_income},
        }
        for unit in [
            "families",
            "marital_units",
            "tax_units",
            "households",
            "spm_units",
        ]:
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


def calculate_consolidated_results(
    reform_name,
    state,
    is_married,
    child_ages,
    income,
    social_security,
    head_age,
    spouse_age=None,
    medical_expenses=0,
    real_estate_taxes=0,
    interest_expense=0,
    charitable_cash=0,
    charitable_non_cash=0,
    qualified_business_income=0,
    casualty_loss=0,
    capital_gains=0,
    spouse_income=0,
    year=AVAILABLE_YEARS[0],
):
    """
    Calculate consolidated results for a given reform and household situation.
    Note: Monetary inputs should already be uprated for the target year.
    """
    if year not in AVAILABLE_YEARS:
        raise ValueError(f"Year must be one of {AVAILABLE_YEARS}")

    # Create situation directly with the provided values (already uprated)
    situation = create_situation(
        state,
        is_married,
        child_ages,
        income,
        social_security,
        head_age,
        spouse_age,
        medical_expenses,
        real_estate_taxes,
        interest_expense,
        charitable_cash,
        charitable_non_cash,
        qualified_business_income,
        casualty_loss,
        capital_gains,  # Added capital_gains here
    )

    if reform_name == "Baseline":
        simulation = Simulation(situation=situation)
    else:
        reform_dict = COMBINED_REFORMS.get(reform_name, {})
        reform = Reform.from_dict(reform_dict, country_id="us")
        simulation = Simulation(reform=reform, situation=situation)

    # Calculate with the specified year
    year_str = str(year)
    
    # Calculate main metrics using the specified year
    household_net_income = simulation.calculate("household_net_income", year_str)[0]
    household_refundable_tax_credits = simulation.calculate(
        "household_refundable_tax_credits", year_str
    )[0]
    household_tax_before_refundable_credits = simulation.calculate(
        "household_tax_before_refundable_credits", year_str
    )[0]

    package = "policyengine_us"
    resource_path_federal = "parameters/gov/irs/credits/refundable.yaml"
    resource_path_state = (
        f"parameters/gov/states/{state.lower()}/tax/income/credits/refundable.yaml"
    )

    try:
        federal_refundable_credits = load_credits_from_yaml(
            package, resource_path_federal
        )
    except FileNotFoundError:
        federal_refundable_credits = []

    try:
        state_refundable_credits = load_credits_from_yaml(package, resource_path_state)
    except FileNotFoundError:
        state_refundable_credits = []

    # Calculate credit breakdowns with the specified year
    federal_credits_dict = calculate_values(
        federal_refundable_credits, simulation, year_str
    )
    state_credits_dict = calculate_values(state_refundable_credits, simulation, year_str)

    # Combine all results
    all_results = {
        "Household Net Income": household_net_income,
        "Income Tax Before Credits": household_tax_before_refundable_credits,
        "Refundable Tax Credits": household_refundable_tax_credits,
        **federal_credits_dict,
        **state_credits_dict,
    }

    # Create DataFrame with all results
    results_df = pd.DataFrame({reform_name: all_results}).T

    return results_df
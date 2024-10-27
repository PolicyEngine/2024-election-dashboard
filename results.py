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
from policyengine_us.variables.household.income.household.household_benefits import (
    household_benefits as HouseholdBenefits,
)
from utils import YEAR, AVAILABLE_YEARS, BASE_YEAR
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
    year=AVAILABLE_YEARS[0],  # Add year parameter with default value
):
    # Convert year to string at the beginning of the function
    year_str = str(year)
    
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
    All monetary inputs are assumed to be in BASE_YEAR dollars and will be uprated to the target year.
    
    Args:
        reform_name: Name of the reform to simulate
        state: State code (e.g., "CA")
        is_married: Boolean indicating marital status
        child_ages: List of ages for children
        income: Employment income (in BASE_YEAR dollars)
        social_security: Social security benefits (in BASE_YEAR dollars)
        head_age: Age of household head
        spouse_age: Age of spouse (if married)
        medical_expenses: Medical expenses (in BASE_YEAR dollars)
        real_estate_taxes: Real estate taxes (in BASE_YEAR dollars)
        interest_expense: Interest expenses (in BASE_YEAR dollars)
        charitable_cash: Cash charitable donations (in BASE_YEAR dollars)
        charitable_non_cash: Non-cash charitable donations (in BASE_YEAR dollars)
        qualified_business_income: Qualified business income (in BASE_YEAR dollars)
        casualty_loss: Casualty losses (in BASE_YEAR dollars)
        capital_gains: Capital gains (in BASE_YEAR dollars)
        spouse_income: Spouse's employment income (in BASE_YEAR dollars)
        year: Target year for simulation (default: first available year)
    
    Returns:
        pandas.DataFrame: Results of the simulation
    """
    if year not in AVAILABLE_YEARS:
        raise ValueError(f"Year must be one of {AVAILABLE_YEARS}")

    # Create a dictionary of all monetary inputs
    monetary_inputs = {
        'income': income,
        'spouse_income': spouse_income,
        'social_security': social_security,
        'capital_gains': capital_gains,
        'medical_expenses': medical_expenses,
        'real_estate_taxes': real_estate_taxes,
        'interest_expense': interest_expense,
        'charitable_cash': charitable_cash,
        'charitable_non_cash': charitable_non_cash,
        'qualified_business_income': qualified_business_income,
        'casualty_loss': casualty_loss,
    }

    # Uprate all monetary inputs from BASE_YEAR to target year
    uprated_values = uprate_inputs(monetary_inputs, BASE_YEAR, year)

    # Create situation with uprated values
    situation = create_situation(
        state=state,
        is_married=is_married,
        child_ages=child_ages,
        income=uprated_values['income'],
        social_security=uprated_values['social_security'],
        head_age=head_age,
        spouse_age=spouse_age,
        medical_expenses=uprated_values['medical_expenses'],
        real_estate_taxes=uprated_values['real_estate_taxes'],
        interest_expense=uprated_values['interest_expense'],
        charitable_cash=uprated_values['charitable_cash'],
        charitable_non_cash=uprated_values['charitable_non_cash'],
        qualified_business_income=uprated_values['qualified_business_income'],
        casualty_loss=uprated_values['casualty_loss'],
        capital_gains=uprated_values['capital_gains'],
        spouse_income=uprated_values['spouse_income'],
        year=year,  # Pass the target year to create_situation
    )

    # Create appropriate simulation based on reform
    if reform_name == "Baseline":
        simulation = Simulation(situation=situation)
    else:
        reform_dict = COMBINED_REFORMS.get(reform_name, {})
        reform = Reform.from_dict(reform_dict, country_id="us")
        simulation = Simulation(reform=reform, situation=situation)

    # Load credit categories
    package = "policyengine_us"
    resource_path_federal = "parameters/gov/irs/credits/refundable.yaml"
    resource_path_state = (
        f"parameters/gov/states/{state.lower()}/tax/income/credits/refundable.yaml"
    )

    try:
        federal_refundable_credits = load_credits_from_yaml(package, resource_path_federal)
    except FileNotFoundError:
        federal_refundable_credits = []

    try:
        state_refundable_credits = load_credits_from_yaml(package, resource_path_state)
    except FileNotFoundError:
        state_refundable_credits = []

    # Get benefit categories
    benefit_categories = HouseholdBenefits.adds

    # Calculate main metrics for the specified year
    household_net_income = simulation.calculate("household_net_income", year)[0]
    household_refundable_tax_credits = simulation.calculate("household_refundable_tax_credits", year)[0]
    household_tax_before_refundable_credits = simulation.calculate("household_tax_before_refundable_credits", year)[0]
    household_benefits = simulation.calculate("household_benefits", year)[0]

    # Calculate breakdowns for the specified year
    federal_credits_dict = calculate_values(federal_refundable_credits, simulation, year)
    state_credits_dict = calculate_values(state_refundable_credits, simulation, year)
    benefits_dict = calculate_values(benefit_categories, simulation, year)

    # Combine all results
    all_results = {
        "Household Net Income": household_net_income,
        "Income Tax Before Credits": household_tax_before_refundable_credits,
        "Refundable Tax Credits": household_refundable_tax_credits,
        "Total Benefits": household_benefits,
        **benefits_dict,
        **federal_credits_dict,
        **state_credits_dict,
    }

    # Create DataFrame with all results
    results_df = pd.DataFrame({reform_name: all_results}).T

    # Print selected columns if this is one of the reforms we want to debug
    if reform_name in ["Baseline", "Harris", "Trump"]:
        print(f"\n=== {reform_name} Results ===")
        selected_columns = [
            "Household Net Income",
            "Income Tax Before Credits",
            "Refundable Tax Credits"
        ]
        print(results_df[selected_columns])
        print("=====================")

    return results_df
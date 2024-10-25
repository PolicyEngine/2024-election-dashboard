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
                    qualified_business_income=0, casualty_loss=0, tip_income=0, overtime_income=0):
    """Create the base situation dictionary following working example structure."""
    
    situation = {
        "people": {
            "you": {
                "age": {YEAR: head_age},
                "employment_income": {YEAR: income},
                "tip_income": {YEAR: tip_income},
                "overtime_income": {YEAR: overtime_income},
                "social_security_retirement": {YEAR: social_security_retirement},
                "medical_out_of_pocket_expenses": {YEAR: medical_expenses},
                "interest_expense": {YEAR: interest_expense},
                "charitable_cash_donations": {YEAR: charitable_cash},
                "charitable_non_cash_donations": {YEAR: charitable_non_cash},
                "qualified_business_income": {YEAR: qualified_business_income},
                "casualty_loss": {YEAR: casualty_loss},
                "real_estate_taxes": {YEAR: real_estate_taxes},
            }
        },
        "families": {
            "your family": {
                "members": ["you"]
            }
        },
        "marital_units": {
            "your marital unit": {
                "members": ["you"]
            }
        },
        "tax_units": {
            "your tax unit": {
                "members": ["you"]
            }
        },
        "spm_units": {
            "your household": {
                "members": ["you"]
            }
        },
        "households": {
            "your household": {
                "members": ["you"],
                "state_name": {YEAR: state}
            }
        }
    }

    # Add children if any
    for i, age in enumerate(child_ages):
        child_id = f"your dependent {i + 1}"
        
        # Add child to people
        situation["people"][child_id] = {
            "age": {YEAR: age},
            "employment_income": {YEAR: 0}
        }
        
        # Add child to family
        situation["families"]["your family"]["members"].append(child_id)
        
        # Create child's marital unit
        situation["marital_units"][f"{child_id}'s marital unit"] = {
            "members": [child_id],
            "marital_unit_id": {YEAR: i + 1}
        }
        
        # Add child to tax unit
        situation["tax_units"]["your tax unit"]["members"].append(child_id)
        
        # Add child to SPM unit and household
        situation["spm_units"]["your household"]["members"].append(child_id)
        situation["households"]["your household"]["members"].append(child_id)

    # Add spouse if married
    if is_married and spouse_age is not None:
        # Add spouse to people
        situation["people"]["your spouse"] = {
            "age": {YEAR: spouse_age},
            "employment_income": {YEAR: 0}
        }
        
        # Add spouse to family
        situation["families"]["your family"]["members"].append("your spouse")
        
        # Add spouse to marital unit
        situation["marital_units"]["your marital unit"]["members"].append("your spouse")
        
        # Add spouse to tax unit
        situation["tax_units"]["your tax unit"]["members"].append("your spouse")
        
        # Add spouse to SPM unit and household
        situation["spm_units"]["your household"]["members"].append("your spouse")
        situation["households"]["your household"]["members"].append("your spouse")

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

def calculate_consolidated_results(reform_name, state, is_married, child_ages, income, 
                                social_security_retirement, head_age, spouse_age=None, 
                                medical_expenses=0, real_estate_taxes=0, interest_expense=0, 
                                charitable_cash=0, charitable_non_cash=0, qualified_business_income=0, 
                                casualty_loss=0, tip_income=0, overtime_income=0):
    """
    Calculates metrics for a single reform with detailed breakdowns.
    """
    # Create situation dictionary
    situation = create_situation(
        state=state,
        is_married=is_married,
        child_ages=child_ages,
        income=income,
        social_security_retirement=social_security_retirement,
        head_age=head_age,
        spouse_age=spouse_age,
        medical_expenses=medical_expenses,
        real_estate_taxes=real_estate_taxes,
        interest_expense=interest_expense,
        charitable_cash=charitable_cash,
        charitable_non_cash=charitable_non_cash,
        qualified_business_income=qualified_business_income,
        casualty_loss=casualty_loss,
        tip_income=tip_income,
        overtime_income=overtime_income
    )
    
    # Set up simulation with reform
    if reform_name == "Baseline":
        reform_dict = COMBINED_REFORMS["Baseline"]
    else:
        reform_dict = COMBINED_REFORMS.get(reform_name, {})
    
    reform = Reform.from_dict(reform_dict, country_id="us")
    simulation = Simulation(reform=reform, situation=situation)

    # Get metrics
    household_net_income = simulation.calculate("household_net_income", YEAR)[0]
    household_refundable_tax_credits = simulation.calculate("household_refundable_tax_credits", YEAR)[0]
    household_tax_before_refundable_credits = simulation.calculate("household_tax_before_refundable_credits", YEAR)[0]

    # Rest of the f
    package = "policyengine_us"
    resource_path_federal = "parameters/gov/irs/credits/refundable.yaml"
    resource_path_state = f"parameters/gov/states/{state.lower()}/tax/income/credits/refundable.yaml"


    # Get categories for credits
    try:
        federal_refundable_credits = load_credits_from_yaml(package, resource_path_federal)
    except FileNotFoundError:
        federal_refundable_credits = []

    try:
        state_refundable_credits = load_credits_from_yaml(package, resource_path_state)
    except FileNotFoundError:
        state_refundable_credits = []

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
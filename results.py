from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from reforms import REFORMS
import pandas as pd

YEAR = "2024"
DEFAULT_AGE = 40

def create_situation(state, num_children, income, rent):
    situation = {
        "people": {
            "you": {
                "age": {YEAR: DEFAULT_AGE},
                "employment_income": {YEAR: income},
                "pre_subsidy_rent": {YEAR: rent}
            },
        },
        "families": {"your family": {"members": ["you"]}},
        "marital_units": {"your marital unit": {"members": ["you"]}},
        "tax_units": {
            "your tax unit": {
                "members": ["you"],
                # Performance improvement settings
                "premium_tax_credit": {YEAR: 0},
                "tax_unit_itemizes": {YEAR: False},
                "taxable_income_deductions_if_itemizing": {YEAR: 0},
                "alternative_minimum_tax": {YEAR: 0},
                "net_investment_income_tax": {YEAR: 0},
            }
        },
        "households": {
            "your household": {"members": ["you"], "state_name": {YEAR: state}}
        },
        "spm_units": {"your household": {"members": ["you"]}},
    }

    for i in range(num_children):
        child_id = f"child_{i}"
        situation["people"][child_id] = {"age": {YEAR: 10}}
        for unit in ["families", "tax_units", "households", "spm_units"]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append(child_id)

    return situation

def run_simulation(reform_name, state, num_children, income, rent):
    reform_dict = REFORMS.get(reform_name, {})
    reform = Reform.from_dict(reform_dict, country_id="us") if reform_dict else None
    
    situation = create_situation(state, num_children, income, rent)
    
    simulation = Simulation(reform=reform, situation=situation)
    result = simulation.calculate("household_net_income", YEAR)
    return result[0]

def calculate_results(selected_reforms, state, num_children, income, rent):
    # Create DataFrame first
    scenarios = ["Baseline"] + selected_reforms
    df = pd.DataFrame(index=scenarios, columns=["Net Income", "Difference", "Percent Change"])
    
    # Calculate baseline
    baseline_income = run_simulation("Baseline", state, num_children, income, rent)
    df.loc["Baseline", "Net Income"] = baseline_income
    df.loc["Baseline", "Difference"] = 0
    df.loc["Baseline", "Percent Change"] = 0
    
    # Calculate individual reforms
    for reform in selected_reforms:
        net_income = run_simulation(reform, state, num_children, income, rent)
        df.loc[reform, "Net Income"] = net_income
        df.loc[reform, "Difference"] = net_income - baseline_income
        df.loc[reform, "Percent Change"] = (net_income - baseline_income) / baseline_income * 100
    
    df = df.reset_index().rename(columns={"index": "Scenario"})
    return df
from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from reforms import REFORMS
from utils import YEAR, DEFAULT_AGE

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

def calculate_results(selected_reforms, state, num_children, income, rent):
    results = {}
    situation = create_situation(state, num_children, income, rent)

    # Calculate baseline
    baseline_simulation = Simulation(situation=situation)
    results["Baseline"] = baseline_simulation.calculate("household_net_income", YEAR)[0]

    # Calculate selected reforms
    for reform_name in selected_reforms:
        reform_dict = REFORMS.get(reform_name, {})
        reform = Reform.from_dict(reform_dict, country_id="us") if reform_dict else None
        simulation = Simulation(reform=reform, situation=situation)
        results[reform_name] = simulation.calculate("household_net_income", YEAR)[0]

    return results

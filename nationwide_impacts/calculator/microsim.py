from policyengine_us import Microsimulation
import pandas as pd
import numpy as np
from nationwide_impacts.calculator.reforms import REFORMS
from policyengine_core.reforms import Reform
import os



def calculate_reform_impact(reform_params=None, year=2025):
    """Calculate impact for a single reform against baseline."""
    if reform_params is None:
        sim = Microsimulation(dataset="cps_2024")
    else:
        reform = Reform.from_dict(reform_params, country_id="us")
        sim = Microsimulation(reform=reform, dataset="cps_2024")
    
    sim.macro_cache_read = False
    
    # Calculate metrics
    net_income = sim.calc("household_net_income", period=year, map_to="household")
    state_code_household = sim.calc("state_code", period=year, map_to="household")
    
    poverty = sim.calc("in_poverty", period=year, map_to="person")
    state_code_person = sim.calc("state_code", period=year, map_to="person")
    
    child = sim.calc("is_child", period=year, map_to="person")
    poverty_gap = sim.calc("poverty_gap", period=year, map_to="household")
    
    personal_hh_equiv_income = sim.calculate("equiv_household_net_income")
    household_count_people = sim.calculate("household_count_people")
    personal_hh_equiv_income.weights *= household_count_people

    return {
        "metrics": pd.DataFrame({
            "net_income": net_income.groupby(state_code_household).sum(),
            "poverty": poverty.groupby(state_code_person).mean(),
            "child_poverty": poverty[child].groupby(state_code_person[child]).mean(),
            "poverty_gap": poverty_gap.groupby(state_code_household).sum(),
            "gini_index": personal_hh_equiv_income.groupby(state_code_household).gini(),
        })
    }

def calculate_all_reform_impacts():
    """
    Calculate impacts for all reforms and save to CSV.
    Results will be stored in data directory in a state-by-reform format.
    """
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    
    year = 2025
    
    print("Calculating baseline...")
    baseline_results = calculate_reform_impact(None, year)
    baseline_metrics = baseline_results["metrics"]
    
    results = []
    
    # Calculate each reform once
    for reform_name, reform_params in REFORMS.items():
        if reform_name == "Baseline":
            continue
            
        print(f"Calculating {reform_name}...")
        reform_results = calculate_reform_impact(reform_params, year)
        reform_metrics = reform_results["metrics"]
        
        # Calculate changes for all states
        for state in reform_metrics.index:
            results.append({
                "state": state,
                "reform_type": reform_name,
                "cost": (
                    reform_metrics.loc[state, "net_income"] - baseline_metrics.loc[state, "net_income"]
                ),
                "poverty_pct_cut": (
                    reform_metrics.loc[state, "poverty"] - baseline_metrics.loc[state, "poverty"]
                ) * 100,
                "child_poverty_pct_cut": (
                    reform_metrics.loc[state, "child_poverty"] - baseline_metrics.loc[state, "child_poverty"]
                ) * 100,
                "poverty_gap_pct_cut": (
                    (reform_metrics.loc[state, "poverty_gap"] - baseline_metrics.loc[state, "poverty_gap"]) /
                    baseline_metrics.loc[state, "poverty_gap"] * 100
                ),
                "gini_index_pct_cut": (
                    reform_metrics.loc[state, "gini_index"] - baseline_metrics.loc[state, "gini_index"]
                )
            })
    
    # Convert to DataFrame and save
    results_df = pd.DataFrame(results)
    results_df.to_csv("data/reform_impacts_2025.csv", index=False)
    print("Results saved to data/reform_impacts_2025.csv")
    
    return results_df

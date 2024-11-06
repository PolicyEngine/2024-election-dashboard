from policyengine_us import Microsimulation
import pandas as pd
import numpy as np
from nationwide_impacts.calculator.reforms import REFORMS
from policyengine_core.reforms import Reform
import os


def calculate_nationwide_enhanced(reform_params=None, year=2025):
    """Calculate nationwide impact using enhanced CPS dataset."""
    if reform_params is None:
        sim = Microsimulation(dataset="enhanced_cps_2024")
    else:
        reform = Reform.from_dict(reform_params, country_id="us")
        sim = Microsimulation(reform=reform, dataset="enhanced_cps_2024")

    sim.macro_cache_read = False

    # Calculate nationwide metrics
    net_income = sim.calc("household_net_income", period=year).sum()

    poverty = sim.calc("in_poverty", period=year, map_to="person").mean()

    personal_hh_equiv_income = sim.calculate("equiv_household_net_income")
    household_count_people = sim.calculate("household_count_people")
    personal_hh_equiv_income.weights *= household_count_people

    return {
        "net_income": net_income,
        "poverty_rate": poverty
    }


def calculate_reform_impact(reform_params=None, year=2025):
    """Calculate impact for a single reform against baseline."""
    # Your existing function remains exactly the same
    if reform_params is None:
        sim = Microsimulation(dataset="pooled_3_year_cps_2023")
    else:
        reform = Reform.from_dict(reform_params, country_id="us")
        sim = Microsimulation(reform=reform, dataset="pooled_3_year_cps_2023")

    sim.macro_cache_read = False

    # Calculate metrics
    net_income = sim.calc("household_net_income", period=year, map_to="household")
    state_code_household = sim.calc("state_code", period=year, map_to="household")

    poverty = sim.calc("in_poverty", period=year, map_to="person")
    state_code_person = sim.calc("state_code", period=year, map_to="person")


    return {
        "metrics": pd.DataFrame(
            {
                "net_income": net_income.groupby(state_code_household).mean(),
                "poverty": poverty.groupby(state_code_person).mean(),
            }
        )
    }


def calculate_all_reform_impacts():
    """Calculate impacts for all reforms and save to CSV files."""
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")

    year = 2025

    # Calculate nationwide impacts using enhanced CPS
    print("Calculating nationwide baseline using enhanced CPS...")
    baseline_enhanced = calculate_nationwide_enhanced(None, year)

    nationwide_results = []

    for reform_name, reform_params in REFORMS.items():
        if reform_name == "Baseline":
            continue

        print(f"Calculating nationwide impacts for {reform_name} using enhanced CPS...")
        reform_enhanced = calculate_nationwide_enhanced(reform_params, year)

        nationwide_results.append(
            {
                "reform_type": reform_name,
                "cost": reform_enhanced["net_income"] - baseline_enhanced["net_income"],
                "poverty_pct_cut": -(
                    (
                        reform_enhanced["poverty_rate"]
                        - baseline_enhanced["poverty_rate"]
                    )
                    / baseline_enhanced["poverty_rate"]
                    * 100
                ),
            }
        )

    # Save nationwide results
    nationwide_df = pd.DataFrame(nationwide_results)
    nationwide_df.to_csv("data/nationwide_impacts_2025.csv", index=False)
    print("Nationwide results saved to data/nationwide_impacts_2025.csv")

    # Calculate state-level impacts (existing functionality)
    print("Calculating state-level baseline...")
    baseline_results = calculate_reform_impact(None, year)
    baseline_metrics = baseline_results["metrics"]

    state_results = []

    for reform_name, reform_params in REFORMS.items():
        if reform_name == "Baseline":
            continue

        print(f"Calculating state-level impacts for {reform_name}...")
        reform_results = calculate_reform_impact(reform_params, year)
        reform_metrics = reform_results["metrics"]

        for state in reform_metrics.index:
            state_results.append(
                {
                    "state": state,
                    "reform_type": reform_name,
                    "cost": (
                        baseline_metrics.loc[state, "net_income"]
                        - reform_metrics.loc[state, "net_income"]
                    ),
                    "poverty_pct_cut": -(
                        (
                            reform_metrics.loc[state, "poverty"]
                            - baseline_metrics.loc[state, "poverty"]
                        )
                    )
                    / baseline_metrics.loc[state, "poverty"]
                    * 100,
                }
            )

    # Save state-level results
    state_results_df = pd.DataFrame(state_results)
    state_results_df.to_csv("data/reform_impacts_2025.csv", index=False)
    print("State-level results saved to data/reform_impacts_2025.csv")

    return state_results_df

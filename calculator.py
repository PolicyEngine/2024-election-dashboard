import pandas as pd
from results import calculate_consolidated_results
from graph import create_reform_comparison_graph
from utils import MAIN_METRICS, format_credit_name, format_currency, STATE_NAMES
import streamlit as st
from policyengine_us.variables.household.income.household.household_benefits import (
    household_benefits as HouseholdBenefits,
)
from utils import format_program_name, format_currency
from results import load_credits_from_yaml


def calculate_reforms(inputs, progress_text, chart_placeholder):
    summary_results = {}

    # Calculate baseline first to get all possible metrics
    progress_text.text("Calculating Baseline...")
    baseline_results = calculate_consolidated_results("Baseline", **inputs)

    # Initialize DataFrame with all metrics from baseline results
    results_df = pd.DataFrame(
        index=baseline_results.columns,
        columns=["Baseline", "Harris", "Trump"],
        dtype=float,
    )

    # Fill in baseline values and show initial results
    for idx in results_df.index:
        results_df.at[idx, "Baseline"] = baseline_results.loc["Baseline", idx]

    summary_results["Baseline"] = results_df.at["Household Net Income", "Baseline"]
    fig = create_reform_comparison_graph(summary_results)
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    # Calculate other reforms
    for reform in ["Harris", "Trump"]:
        progress_text.text(f"Calculating {reform}...")
        reform_results = calculate_consolidated_results(reform, **inputs)

        # Update results for all metrics
        for idx in results_df.index:
            if idx in reform_results.columns:
                results_df.at[idx, reform] = reform_results.loc[reform, idx]

        # Update summary for chart
        summary_results[reform] = results_df.at["Household Net Income", reform]

        # Update chart
        fig = create_reform_comparison_graph(summary_results)
        chart_placeholder.plotly_chart(fig, use_container_width=True)

    return summary_results, results_df


def format_detailed_metrics(results_df):
    formatted_df = results_df.copy()
    formatted_df = formatted_df.loc[MAIN_METRICS]
    formatted_df = formatted_df.round(2)
    formatted_df = formatted_df.applymap(format_currency)
    return formatted_df


def format_federal_credit_components(results_df):
    """Format federal credit components, showing items with baseline or reform values"""
    formatted_df = results_df.copy()

    # Get credits loaded from federal YAML file
    package = "policyengine_us"
    resource_path_federal = "parameters/gov/irs/credits/refundable.yaml"
    try:
        federal_refundable_credits = load_credits_from_yaml(
            package, resource_path_federal
        )
    except FileNotFoundError:
        federal_refundable_credits = []

    # Get credits that are in the federal YAML
    federal_credit_rows = [
        idx
        for idx in formatted_df.index
        if idx not in MAIN_METRICS and idx in federal_refundable_credits
    ]

    if not federal_credit_rows:
        return None

    # Keep only credits with values
    formatted_df = formatted_df.loc[federal_credit_rows]
    formatted_df = formatted_df.round(2)
    formatted_df = formatted_df.applymap(format_currency)

    # Format index names
    formatted_df.index = [format_credit_name(idx) for idx in formatted_df.index]

    return formatted_df


def format_state_credit_components(results_df, state_code):
    """Format state credit components, showing items with baseline or reform values"""
    formatted_df = results_df.copy()

    # Get credits loaded from state YAML file
    package = "policyengine_us"
    resource_path_state = (
        f"parameters/gov/states/{state_code.lower()}/tax/income/credits/refundable.yaml"
    )
    try:
        state_refundable_credits = load_credits_from_yaml(package, resource_path_state)
    except FileNotFoundError:
        state_refundable_credits = []

    # Get credits that are in the state YAML
    state_credit_rows = [
        idx
        for idx in formatted_df.index
        if idx not in MAIN_METRICS and idx in state_refundable_credits
    ]

    if not state_credit_rows:
        return None

    # Keep only credits with values
    formatted_df = formatted_df.loc[state_credit_rows]
    formatted_df = formatted_df.round(2)
    formatted_df = formatted_df.applymap(format_currency)

    # Format index names with state name
    formatted_df.index = [
        format_credit_name(idx, state_code) for idx in formatted_df.index
    ]

    return formatted_df


def format_benefits_components(results_df):
    """Format the benefits breakdown showing all non-zero benefits"""
    formatted_df = results_df.copy()

    # List of known benefit names
    benefits = [
        "snap",
        "tanf",
        "ssi",
        "housing_vouchers",
        "medicaid",
        "medicare",
        "social_security",
        "unemployment_compensation",
        "wic",
        "free_school_meals",
        "reduced_price_school_meals",
        "spm_unit_broadband_subsidy",
        "high_efficiency_electric_home_rebate",
        "residential_efficiency_electrification_rebate",
        "head_start",
        "early_head_start",
    ]

    # Get all benefits that appear in the results
    benefit_rows = [
        idx
        for idx in formatted_df.index
        if idx in benefits and any(formatted_df.loc[idx] != 0)
    ]

    if not benefit_rows:
        return None

    # Keep only benefits with values
    formatted_df = formatted_df.loc[benefit_rows]
    formatted_df = formatted_df.round(2)
    formatted_df = formatted_df.applymap(format_currency)

    # Format index names using program name formatter
    formatted_df.index = [format_program_name(idx) for idx in formatted_df.index]

    # Sort by baseline values
    formatted_df = formatted_df.sort_values("Baseline", ascending=False)

    return formatted_df

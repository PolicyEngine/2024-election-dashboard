import pandas as pd
from results import calculate_consolidated_results
from graph import create_reform_comparison_graph
from utils import MAIN_METRICS, format_credit_name, format_currency, uprate_inputs, BASE_YEAR
import streamlit as st
from policyengine_us.variables.household.income.household.household_benefits import (
    household_benefits as HouseholdBenefits,
)
from utils import format_program_name, format_currency

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


def format_credit_components(results_df, state_code):
    """Format credit components, showing items with baseline or reform values"""
    formatted_df = results_df.copy()
    
    # Get all credits (excluding main metrics)
    credit_rows = [idx for idx in formatted_df.index 
                   if idx not in MAIN_METRICS and 
                   "benefits" not in idx.lower()]
    
    # Filter credit components that have any non-zero value in baseline or reforms
    active_credits = []
    for idx in credit_rows:
        if idx in formatted_df.index:
            # Check if there's a value in baseline OR any reform
            baseline_value = formatted_df.loc[idx, "Baseline"] != 0
            reform_value = (formatted_df.loc[idx, ["Harris", "Trump"]] != 0).any()
            if baseline_value or reform_value:
                active_credits.append(idx)
    
    if not active_credits:
        return None
    
    # Keep only credits with values
    formatted_df = formatted_df.loc[active_credits]
    formatted_df = formatted_df.round(2)
    formatted_df = formatted_df.applymap(format_currency)
    
    # Format index names with state name for state credits
    formatted_df.index = [format_credit_name(idx, state_code) for idx in formatted_df.index]
    
    return formatted_df

def format_benefits_components(results_df):
    """Format the benefits breakdown using HouseholdBenefits categories"""
    formatted_df = results_df.copy()
    
    # Get benefit categories from HouseholdBenefits
    benefit_categories = HouseholdBenefits.adds
    
    # Get all benefits using these categories (excluding main metrics)
    benefit_rows = [idx for idx in formatted_df.index 
                   if idx in benefit_categories]
    
    # Filter benefits that exist in baseline
    active_benefits = []
    for idx in benefit_rows:
        if idx in formatted_df.index:
            # Only check baseline value
            has_value = formatted_df.loc[idx, "Baseline"] != 0
            if has_value:
                active_benefits.append(idx)
    
    if not active_benefits:
        return None
    
    # Keep only benefits with baseline values
    formatted_df = formatted_df.loc[active_benefits]
    formatted_df = formatted_df.round(2)
    formatted_df = formatted_df.applymap(format_currency)
    
    # Format index names using program name formatter
    formatted_df.index = [format_program_name(idx) for idx in formatted_df.index]
    
    # Sort by baseline values
    formatted_df = formatted_df.sort_values("Baseline", ascending=False)
    
    return formatted_df
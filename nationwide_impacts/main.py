import streamlit as st
import pandas as pd
from nationwide_impacts.calculator.reforms import REFORMS
from nationwide_impacts.map import render_reform_map
from .utils import REFORM_DETAILS, TECHNICAL_NOTES


def render_nationwide_impacts():
    st.title("Tax Reform Impact Calculator")

    # Add description
    st.write(
        """
    This calculator shows the impact of various tax reform proposals on the budget, poverty, and inequality in 2025.
    Select a reform to analyze its effects.
    """
    )

    # Load pre-calculated results
    nationwide_results_df = pd.read_csv("data/nationwide_impacts_2025.csv")
    state_results_df = pd.read_csv("data/reform_impacts_2025.csv")

    # Create columns for selectors
    col1, col2 = st.columns(2)

    # Reform selector in first column
    reform_options = list(REFORMS.keys())
    reform_options.remove("Baseline")  # Remove baseline as it's not in results
    
    with col1:
        selected_reform = st.selectbox(
            "Select a reform to view impacts:",
            options=reform_options
        )
        st.session_state.selected_reform = selected_reform

    # Metric selector in second column
    METRICS = {
        "Average Household Impact ($)": "cost",
        "Poverty Reduction (%)": "poverty_pct_cut",
        "Gini Index Reduction (%)": "gini_index_pct_cut",
    }
    
    with col2:
        selected_metric_name = st.selectbox(
            "Select Metric:",
            options=list(METRICS.keys())
        )
    st.session_state.selected_metric = selected_metric_name
    st.session_state.selected_metric_column = METRICS[selected_metric_name]

    # Add map visualization
    render_reform_map()

    # Create state-level table in an expander
    with st.expander("View Detailed State-Level Data", expanded=False):
        # Convert cost to billions before creating table
        reform_results["cost"] = reform_results["cost"]

        state_table = reform_results[
            [
                "state",
                "cost",
                "poverty_pct_cut",
                "gini_index_pct_cut",
            ]
        ].copy()

        # Rename columns for display
        state_table.columns = [
            "State",
            "Average Household Impact ($)",
            "Poverty Reduction (%)",
            "Gini Index Reduction (%)",
        ]

        # Display state results in an interactive table
        st.dataframe(state_table.round(2), hide_index=True, use_container_width=True)

    # Display nationwide results
    st.header("Nationwide Impacts")
    col1, col2 = st.columns(2)

    with col1:
        # Calculate the value first
        budget_value = nationwide_reform_results["cost"] / 1e9
        # Format with negative sign in front of dollar sign if negative
        budget_display = (
            f"-${abs(budget_value):.1f}B"
            if budget_value < 0
            else f"${budget_value:.1f}B"
        )

        st.metric(
            "Budgetary Impact",
            budget_display,
            delta=None,
        )

        st.metric(
            "Poverty Rate Reduction",
            f"{nationwide_reform_results['poverty_pct_cut']:.1f}%",
            delta=None,
        )
        st.metric(
            "Child Poverty Reduction",
            f"{nationwide_reform_results['child_poverty_pct_cut']:.1f}%",
            delta=None,
        )

    with col2:
        st.metric(
            "Poverty Gap Reduction",
            f"{nationwide_reform_results['poverty_gap_pct_cut']:.1f}%",
            delta=None,
        )
        st.metric(
            "Gini Index Reduction",
            f"{nationwide_reform_results['gini_index_pct_cut']:.1f}%",
            delta=None,
        )

    with st.expander("Reform Details & Policy Explanations"):
        st.markdown(REFORM_DETAILS)

    with st.expander("Technical Notes & Assumptions"):
        st.markdown(TECHNICAL_NOTES)

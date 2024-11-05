import streamlit as st
import pandas as pd
from nationwide_impacts.calculator.reforms import REFORMS
from nationwide_impacts.map import render_reform_map


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

    # Reform selector
    reform_options = list(REFORMS.keys())
    reform_options.remove("Baseline")  # Remove baseline as it's not in results
    selected_reform = st.selectbox(
        "Select a reform package to view impacts:", options=reform_options
    )
    st.session_state.selected_reform = selected_reform

    # Get nationwide results for selected reform
    nationwide_reform_results = nationwide_results_df[
        nationwide_results_df["reform_type"] == selected_reform
    ].iloc[0]

    # Get state results for selected reform
    reform_results = state_results_df[
        state_results_df["reform_type"] == selected_reform
    ].copy()

    # Display nationwide results
    st.header("Nationwide Impacts")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Budgetary Impact",
            f"${nationwide_reform_results['cost']/1e9:.1f}B",
            delta=None,
        )
        st.metric(
            "Change in Poverty Rate",
            f"{nationwide_reform_results['poverty_pct_cut']:.2f}%",
            delta=None,
        )
        st.metric(
            "Change in Child Poverty Rate",
            f"{nationwide_reform_results['child_poverty_pct_cut']:.2f}%",
            delta=None,
        )

    with col2:
        st.metric(
            "Change in Poverty Gap",
            f"{nationwide_reform_results['poverty_gap_pct_cut']:.1f}%",
            delta=None,
        )
        st.metric(
            "Change in Gini Index",
            f"{nationwide_reform_results['gini_index_pct_cut']/100:.4f}",
            delta=None,
        )

    # Add map visualization
    st.header("State-Level Impacts")
    render_reform_map()

    # Create state-level table in an expander
    with st.expander("View Detailed State-Level Data", expanded=False):
        # Convert cost to billions before creating table
        reform_results["cost"] = reform_results["cost"] / 1e9

        state_table = reform_results[
            [
                "state",
                "cost",
                "poverty_pct_cut",
                "child_poverty_pct_cut",
                "poverty_gap_pct_cut",
                "gini_index_pct_cut",
            ]
        ].copy()

        # Rename columns for display
        state_table.columns = [
            "State",
            "Budgetary Impact ($B)",
            "Poverty Change (%)",
            "Child Poverty Change (%)",
            "Poverty Gap Change (%)",
            "Gini Index Change",
        ]

        # Display state results in an interactive table
        st.dataframe(state_table.round(2), hide_index=True, use_container_width=True)

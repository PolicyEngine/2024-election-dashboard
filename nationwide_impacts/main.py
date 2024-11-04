import streamlit as st
import pandas as pd
from nationwide_impacts.calculator.reforms import REFORMS
from nationwide_impacts.map import render_reform_map

def render_nationwide_impacts():
    st.title("Tax Reform Impact Calculator")
    
    # Add description
    st.write("""
    This calculator shows the impact of various tax reform proposals on poverty, inequality, and household income.
    Select a reform package to analyze its effects.
    """)
    
    # Load pre-calculated results
    results_df = pd.read_csv("data/reform_impacts_2025.csv")
    
    # Reform selector
    reform_options = list(REFORMS.keys())
    reform_options.remove("Baseline")  # Remove baseline as it's not in results
    selected_reform = st.selectbox(
        "Select a reform package to view impacts:",
        options=reform_options
    )
    st.session_state.selected_reform = selected_reform
    
    # Get results for selected reform
    reform_results = results_df[results_df['reform_type'] == selected_reform].copy()
    
    # Calculate national averages
    national_results = {
        "budgetary_impact_billions": reform_results['cost'].mean() / 1e9,
        "poverty_rate_change_pct": reform_results['poverty_pct_cut'].mean(),
        "child_poverty_rate_change_pct": reform_results['child_poverty_pct_cut'].mean(),
        "poverty_gap_change_billions": reform_results['poverty_gap_pct_cut'].mean() / 100,
        "gini_change": reform_results['gini_index_pct_cut'].mean() / 100
    }
    
    # Display national results
    st.header("National Impacts")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Budgetary Impact", 
            f"${national_results['budgetary_impact_billions']:.1f}B",
            delta=None
        )
        st.metric(
            "Change in Poverty Rate", 
            f"{national_results['poverty_rate_change_pct']:.2f}pp",
            delta=None
        )
        st.metric(
            "Change in Child Poverty Rate", 
            f"{national_results['child_poverty_rate_change_pct']:.2f}pp",
            delta=None
        )
    
    with col2:
        st.metric(
            "Change in Poverty Gap", 
            f"{national_results['poverty_gap_change_billions']:.1f}pp",
            delta=None
        )
        st.metric(
            "Change in Gini Index", 
            f"{national_results['gini_change']:.4f}",
            delta=None
        )
    
    # Display state-level results
    st.header("State-Level Impacts")
    

    # Add map visualization
    st.header("State-Level Impacts")
    render_reform_map()

    # Create state-level table
    state_table = reform_results[['state', 'poverty_pct_cut', 'child_poverty_pct_cut', 
                                'poverty_gap_pct_cut', 'gini_index_pct_cut']].copy()
    
    # Rename columns for display
    state_table.columns = ['State', 'Poverty Change (%)', 'Child Poverty Change (%)',
                          'Poverty Gap Change (%)', 'Gini Index Change']
    
    # Display state results in an interactive table
    st.dataframe(
        state_table.round(2),
        hide_index=True,
        use_container_width=True
    )

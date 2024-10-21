import streamlit as st
import pandas as pd
from results import calculate_results
from config import REFORMS, APP_TITLE, NOTES, REFORMS_DESCRIPTION
from utils import STATE_CODES, YEAR
from graph import create_reform_comparison_graph  # Import the graph function from graph.py

# Main streamlit application logic
st.set_page_config(page_title=APP_TITLE, page_icon="👪", layout="wide")
st.title(APP_TITLE)

# Display the reform description (this is the exact content from REFORMS_DESCRIPTION)
st.markdown(REFORMS_DESCRIPTION)

# Input sections for the user
col1, col2 = st.columns(2)

with col1:
    is_married = st.checkbox("I am married")
    state = st.selectbox("State of residence", STATE_CODES)
    num_children = st.number_input("Number of Children", min_value=0, max_value=10, value=0, step=1)

    # Inputs for child ages
    child_ages = []
    if num_children > 0:
        age_cols = st.columns(min(num_children, 3))  # Up to 3 columns for child ages
        for i in range(num_children):
            with age_cols[i % 3]:
                age = st.number_input(f"Age Child {i+1}", min_value=0, max_value=18, value=5, key=f"child_{i}")
                child_ages.append(age)

with col2:
    income = st.slider("Household annual wages and salaries", min_value=0, max_value=500000, value=50000, step=500, format="$%d")
    social_security_retirement = st.slider("Household annual social security retirement income", min_value=0, max_value=100000, value=0, step=500, format="$%d")
    rent = st.slider("Household annual rent", min_value=0, max_value=120000, value=12000, step=500, format="$%d")
    fair_market_rent = st.number_input("Estimated small area fair market rent", min_value=0, max_value=120000, value=12000, step=500)

# Section for reform selection
st.markdown("## Select Reforms to Compare")
available_reforms = list(REFORMS.keys())[1:]  # Exclude Baseline

# Separate reforms into two groups for selection
harris_walz_reforms = [reform for reform in available_reforms if any(name in reform for name in ['Harris', 'Walz'])]
trump_vance_reforms = [reform for reform in available_reforms if any(name in reform for name in ['Trump', 'Vance'])]

selected_reforms = []
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Harris/Walz Reforms")
    for reform in harris_walz_reforms:
        if st.checkbox(REFORMS[reform]['name'], key=f"reform_{reform}"):
            selected_reforms.append(reform)

with col2:
    st.markdown("### Trump/Vance Reforms")
    for reform in trump_vance_reforms:
        if st.checkbox(REFORMS[reform]['name'], key=f"reform_{reform}"):
            selected_reforms.append(reform)

# Calculation button
if st.button("Calculate my household income"):


    # Placeholder for the chart
    chart_placeholder = st.empty()

    # Initial calculation (Baseline)
    results = calculate_results(['Baseline'], state, is_married, child_ages, income, rent, fair_market_rent, social_security_retirement)
    
    # Display baseline chart
    fig = create_reform_comparison_graph(results)
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    # Calculate each selected reform and update the chart
    for reform_key in selected_reforms:
        # Perform calculation for the selected reform
        reform_results = calculate_results([reform_key], state, is_married, child_ages, income, rent, fair_market_rent, social_security_retirement)
        results[reform_key] = reform_results[reform_key]

        # Update chart with new reform results
        fig = create_reform_comparison_graph(results)
        chart_placeholder.plotly_chart(fig, use_container_width=True)

st.markdown(NOTES)

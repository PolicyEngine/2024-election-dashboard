import streamlit as st
import pandas as pd
from results import calculate_results, calculate_detailed_metrics
from reforms import COMBINED_REFORMS
from config import APP_TITLE, NOTES, REFORMS_DESCRIPTION, BASELINE_DESCRIPTION
from utils import STATE_CODES, YEAR
from graph import create_reform_comparison_graph

# Main streamlit application logic
st.set_page_config(page_title=APP_TITLE, page_icon="👪", layout="wide")
st.title(APP_TITLE)

st.markdown(BASELINE_DESCRIPTION)

st.markdown("## Enter your current household information")

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
    income = st.slider("Annual wages and salaries", min_value=0, max_value=500000, value=50000, step=500, format="$%d")
    social_security_retirement = st.slider("Annual social security retirement income", min_value=0, max_value=100000, value=0, step=500, format="$%d")

# Calculation button
if st.button("Calculate my household income"):
    # Placeholder for the chart and progress
    chart_placeholder = st.empty()
    progress_text = st.empty()

    # Initialize results dictionary
    results = {}

    # Calculate baseline first
    progress_text.text("Calculating baseline...")
    baseline_results = calculate_results(
        ["Baseline"],
        state,
        is_married,
        child_ages,
        income,
        social_security_retirement
    )
    results["Baseline"] = baseline_results["Baseline"]
    
    # Display baseline chart
    fig = create_reform_comparison_graph(results)
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    # Calculate Harris-Walz reforms
    progress_text.text("Calculating Harris-Walz reforms...")
    harris_results = calculate_results(
        ["Harris-Walz"],
        state,
        is_married,
        child_ages,
        income,
        social_security_retirement
    )
    results["Harris-Walz"] = harris_results["Harris-Walz"]
    
    # Update chart with Harris-Walz results
    fig = create_reform_comparison_graph(results)
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    # Calculate Trump-Vance reforms
    progress_text.text("Calculating Trump-Vance reforms...")
    trump_results = calculate_results(
        ["Trump-Vance"],
        state,
        is_married,
        child_ages,
        income,
        social_security_retirement
    )
    results["Trump-Vance"] = trump_results["Trump-Vance"]
    
    # Final chart update with all results
    fig = create_reform_comparison_graph(results)
    chart_placeholder.plotly_chart(fig, use_container_width=True)
    
    # Clear the progress text
    progress_text.empty()

    # Display reform descriptions after the chart
    st.markdown("## Reform Details")
    st.markdown(REFORMS_DESCRIPTION)
    
    # Show calculation progress after reform descriptions
    progress_text.text("Calculating detailed breakdown metrics...")

    # Calculate and display detailed metrics
    detailed_df = calculate_detailed_metrics(
        state,
        is_married,
        child_ages,
        income,
        social_security_retirement
    )
    
    # Format values with rounding
    formatted_df = pd.DataFrame(
        index=detailed_df.index,
        columns=detailed_df.columns
    )
    
    for idx in detailed_df.index:
        for col in detailed_df.columns:
            value = detailed_df.at[idx, col]
            formatted_df.at[idx, col] = f"${round(value):,}"
    
    # Clear progress text
    progress_text.empty()
    
    # Display the table followed by notes
    st.markdown(formatted_df.to_markdown())
    st.markdown(NOTES)
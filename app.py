import streamlit as st
from ui_components import (
    render_personal_info,
    render_income_inputs,
    render_itemized_deductions,
)
from calculator import (
    calculate_reforms,
    format_detailed_metrics,
    format_credit_components,
)
from config import APP_TITLE, NOTES, REFORMS_DESCRIPTION, BASELINE_DESCRIPTION
from utils import AVAILABLE_YEARS, BASE_YEAR, uprate_inputs

# Page setup
st.set_page_config(page_title=APP_TITLE, page_icon="👪", layout="wide")
st.title(APP_TITLE)
st.markdown(BASELINE_DESCRIPTION)

# In app.py - Update year selector
selected_year = st.selectbox(
    "Select policy year",
    AVAILABLE_YEARS,
    index=0,  # Default to 2025
    help="Select the year for which you want to calculate policy impacts. Your input values will be automatically adjusted for inflation from 2024."
)

st.markdown(f"## Enter your household information for {BASE_YEAR}")
st.markdown(f"*Values will be automatically adjusted for inflation to {selected_year}*")

# Render form sections
personal_col, income_col = st.columns(2)

with personal_col:
    st.markdown("### Personal Information")
    is_married, state, child_ages, head_age, spouse_age = render_personal_info()

with income_col:
    st.markdown("### Income Information")
    income, social_security, capital_gains, spouse_income = render_income_inputs(is_married)
    itemized_deductions = render_itemized_deductions()

# Calculate button
if st.button("Calculate my household income"):
    chart_placeholder = st.empty()
    progress_text = st.empty()

    # First collect all non-monetary inputs
    base_inputs = {
        "state": state,
        "is_married": is_married,
        "child_ages": child_ages,
        "head_age": head_age,
        "spouse_age": spouse_age,
    }
    
    # Collect all monetary inputs (these will be uprated)
    monetary_inputs = {
        "income": income,
        "spouse_income": spouse_income,
        "social_security": social_security,
        "capital_gains": capital_gains,
        **itemized_deductions,  # Contains all the itemized deduction amounts
    }

    # Combine all inputs
    inputs = {
        **base_inputs,
        **monetary_inputs,
        "year": selected_year,  # Add selected year
    }

    # Calculate and display results
    summary_results, results_df = calculate_reforms(
        inputs, 
        progress_text, 
        chart_placeholder,
    )

    # Display reform details
    st.markdown("## Reform Details")
    st.markdown(REFORMS_DESCRIPTION)

    # Create tabs for main metrics and credit components
    tab1, tab2 = st.tabs(["Main Breakdown", "Refundable Credits"])

    with tab1:
        # Display main metrics
        formatted_df = format_detailed_metrics(results_df)
        st.markdown(formatted_df.to_markdown())

    with tab2:
        # Display credit components
        credit_df = format_credit_components(results_df, state)
        if credit_df is not None:
            st.markdown(credit_df.to_markdown())
        else:
            st.markdown("### No changes in credit components")

    st.markdown(NOTES)
    progress_text.empty()
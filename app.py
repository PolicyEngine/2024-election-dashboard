import streamlit as st
from ui_components import render_personal_info, render_income_inputs, render_itemized_deductions
from calculator import calculate_reforms, format_detailed_metrics
from config import APP_TITLE, NOTES, REFORMS_DESCRIPTION, BASELINE_DESCRIPTION

# Page setup
st.set_page_config(page_title=APP_TITLE, page_icon="👪", layout="wide")
st.title(APP_TITLE)
st.markdown(BASELINE_DESCRIPTION)
st.markdown("## Enter your current household information")

# Render form sections
personal_col, income_col = st.columns(2)

with personal_col:
    st.markdown("### Personal Information")
    is_married, state, child_ages, head_age, spouse_age = render_personal_info()

with income_col:
    st.markdown("### Income Information")
    income, social_security_retirement = render_income_inputs()
    itemized_deductions = render_itemized_deductions()

# Calculate button
if st.button("Calculate my household income"):
    chart_placeholder = st.empty()
    progress_text = st.empty()
    
    # Prepare inputs
    inputs = {
        "state": state,
        "is_married": is_married,
        "child_ages": child_ages,
        "head_age": head_age,
        "spouse_age": spouse_age,
        "income": income,
        "social_security_retirement": social_security_retirement,
        **itemized_deductions
    }
    
    # Calculate and display results
    summary_results, results_df = calculate_reforms(inputs, progress_text, chart_placeholder)
    
    # Display reform details
    st.markdown("## Reform Details")
    st.markdown(REFORMS_DESCRIPTION)
    
    # Format and display detailed metrics
    formatted_df = format_detailed_metrics(results_df)
    st.markdown(formatted_df.to_markdown())
    st.markdown(NOTES)
    
    progress_text.empty()
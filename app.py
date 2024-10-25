import streamlit as st
from ui_components import render_personal_info, render_income_inputs, render_itemized_deductions
from calculator import calculate_reforms, format_detailed_metrics, format_credit_components
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
    # Update to unpack all four return values
    income, social_security_retirement, tip_income, overtime_income = render_income_inputs()
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
        "tip_income": tip_income,
        "overtime_income": overtime_income,
        **itemized_deductions
    }
    
    # Calculate and display results
    summary_results, results_df = calculate_reforms(inputs, progress_text, chart_placeholder)
    
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
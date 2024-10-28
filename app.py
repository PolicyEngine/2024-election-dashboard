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
    format_benefits_components,
)
from config import (
    APP_TITLE,
    NOTES,
    REFORMS_DESCRIPTION,
    BASELINE_DESCRIPTION,
    ADDITIONAL_POLICIES,
)


# Page setup
st.set_page_config(page_title=APP_TITLE, page_icon="👪", layout="wide")
st.title(APP_TITLE)
st.markdown(BASELINE_DESCRIPTION)
st.markdown("## Enter your current household information")
st.markdown("*Please enter annual amounts for the tax year 2024*")

# Render form sections
personal_col, income_col = st.columns(2)

with personal_col:
    st.markdown("### Personal Information")
    personal_info = render_personal_info()
    is_married, state, child_ages, head_age, spouse_age, in_nyc = personal_info

with income_col:
    st.markdown("### Income Information")
    (
        income,
        tip_income,
        overtime_income,
        social_security,
        capital_gains,
        spouse_income,
    ) = render_income_inputs(is_married)
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
        "spouse_income": spouse_income,
        "social_security": social_security,
        "capital_gains": capital_gains,
        "tip_income": tip_income,
        "overtime_income": overtime_income,
        "in_nyc": in_nyc,  # Add the NYC parameter
        **itemized_deductions,
    }

    # Calculate and display results
    summary_results, results_df = calculate_reforms(
        inputs, progress_text, chart_placeholder
    )


    # Display reform details
    st.markdown("## Reform Details")
    st.markdown(REFORMS_DESCRIPTION)

    # Create tabs for different breakdowns
    tab1, tab2, tab3 = st.tabs(["Main Breakdown", "Benefits", "Refundable Credits"])

    with tab1:
        # Display main metrics
        formatted_df = format_detailed_metrics(results_df)
        st.markdown(formatted_df.to_markdown())

    with tab2:
        # Display benefits breakdown
        benefits_df = format_benefits_components(results_df)
        if benefits_df is not None:
            st.markdown(benefits_df.to_markdown())
        else:
            st.markdown("### No changes in benefits")

    with tab3:
        # Display credit components
        credit_df = format_credit_components(results_df, state)
        if credit_df is not None:
            st.markdown(credit_df.to_markdown())
        else:
            st.markdown("### No changes in credit components")

    with st.expander("View Additional Tax & Benefit Proposals (Not Currently Modeled)"):
        st.markdown(ADDITIONAL_POLICIES)

    st.markdown(NOTES)
    progress_text.empty()

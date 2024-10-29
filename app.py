import streamlit as st
from ui_components import (
    render_personal_info,
    render_income_inputs,
    render_itemized_deductions,
)
from calculator import (
    calculate_reforms,
    format_detailed_metrics,
    format_federal_credit_components,
    format_state_credit_components,
    format_benefits_components,
    format_tax_components,
)
from config import (
    APP_TITLE,
    NOTES,
    BASELINE_DESCRIPTION,
    ADDITIONAL_POLICIES,
)


# Page setup
st.set_page_config(page_title=APP_TITLE, page_icon="👪", layout="wide")
st.title(APP_TITLE)
st.markdown(BASELINE_DESCRIPTION)
st.markdown("## Enter your current household information")
st.markdown("*Please enter estimated annual amounts for the tax year 2025*")

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

    # Create tabs for different breakdowns
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Main Breakdown",
            "Taxes",
            "Benefits",
            "Federal Refundable Credits",
            "State Refundable Credits",
        ]
    )
    with tab1:
        # Display main metrics
        formatted_df = format_detailed_metrics(results_df)
        st.markdown(formatted_df.to_markdown())

    with tab2:
        # Display tax breakdown
        tax_df = format_tax_components(results_df)
        if tax_df is not None:
            st.markdown(tax_df.to_markdown())
        else:
            st.markdown("### No applicable income tax")

    with tab3:
        # Display benefits breakdown
        benefits_df = format_benefits_components(results_df)
        if benefits_df is not None:
            st.markdown(benefits_df.to_markdown())
        else:
            st.markdown("### No Benefits available")

    with tab4:
        # Display federal credit components
        federal_credit_df = format_federal_credit_components(results_df)
        if federal_credit_df is not None:
            st.markdown(federal_credit_df.to_markdown())
        else:
            st.markdown("### No federal credits available")

    with tab5:
        # Display state credit components
        state_credit_df = format_state_credit_components(results_df, state)
        if state_credit_df is not None:
            st.markdown(state_credit_df.to_markdown())
        else:
            st.markdown("### No state credits available")

    with st.expander("View Additional Tax & Benefit Proposals (Not Currently Modeled)"):
        st.markdown(ADDITIONAL_POLICIES)

    st.markdown(NOTES)
    progress_text.empty()

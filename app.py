import streamlit as st
from ui_components import (
    render_personal_info,
    render_income_inputs,
    render_itemized_deductions,
    render_import_expenses,
)
from calculator import (
    calculate_reforms,
    format_detailed_metrics,
    format_federal_credit_components,
    format_state_credit_components,
    format_benefits_components,
    format_tax_components,
    format_tariff_components,
)
from config import (
    APP_TITLE,
    NOTES,
    BASELINE_DESCRIPTION,
    ADDITIONAL_POLICIES,
    REFORMS_DESCRIPTION,
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
    (
        is_married,
        state,
        child_ages,
        head_age,
        spouse_age,
        in_nyc,
    ) = personal_info

with income_col:
    st.markdown("### Income Information")
    (
        income,
        tip_income,
        overtime_income,
        social_security,
        capital_gains,
        dividend_income,
    ) = render_income_inputs(is_married)
    itemized_deductions = render_itemized_deductions()

china_imports, other_imports = render_import_expenses()


# Calculate button
if st.button("Calculate my household income"):
    chart_placeholder = st.empty()
    progress_text = st.empty()

    # Prepare inputs and calculate results
    inputs = {
        "state": state,
        "is_married": is_married,
        "child_ages": child_ages,
        "head_age": head_age,
        "spouse_age": spouse_age,
        "income": income,
        "social_security": social_security,
        "capital_gains": capital_gains,
        "dividend_income": dividend_income,
        "tip_income": tip_income,
        "overtime_income": overtime_income,
        "in_nyc": in_nyc,
        **itemized_deductions,
        "china_imports": china_imports,
        "other_imports": other_imports,
    }

    # Calculate and display results
    summary_results, results_df = calculate_reforms(
        inputs, progress_text, chart_placeholder
    )

    # Create tabs for all breakdowns
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Main Breakdown",
            "Taxes",
            "Tariffs",
            "Benefits",
            "Federal Refundable Credits",
            "State Refundable Credits",
        ]
    )

    with tab1:
        # Display main metrics in first tab
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
        # Display tariffs breakdown
        tariffs_df = format_tariff_components(results_df)
        if tariffs_df is not None:
            st.markdown("### Import Tariffs")
            st.markdown(tariffs_df.to_markdown())
        else:
            st.markdown("### No tariffs applicable")

    with tab4:
        # Display benefits breakdown
        benefits_df = format_benefits_components(results_df)
        if benefits_df is not None:
            st.markdown(benefits_df.to_markdown())
        else:
            st.markdown("### No Benefits available")

    with tab5:
        # Display federal credit components
        federal_credit_df = format_federal_credit_components(results_df)
        if federal_credit_df is not None:
            st.markdown(federal_credit_df.to_markdown())
        else:
            st.markdown("### No federal credits available")

    with tab6:
        # Display state credit components
        state_credit_df = format_state_credit_components(results_df, state)
        if state_credit_df is not None:
            st.markdown(state_credit_df.to_markdown())
        else:
            st.markdown("### No state credits available")

    # Add collapsible sections after tabs
    with st.expander("Policy Proposals modeled in this calculator"):
        st.markdown(REFORMS_DESCRIPTION)

    with st.expander("View Additional Tax & Benefit Proposals (Not Currently Modeled)"):
        st.markdown(ADDITIONAL_POLICIES)

    with st.expander("Assumptions and Notes"):
        st.markdown(NOTES)

    progress_text.empty()

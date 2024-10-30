import streamlit as st
from utils import STATE_CODES, format_currency


def render_personal_info():
    is_married = st.checkbox("I am married")

    # Create two small columns for age inputs
    age_col1, age_col2 = st.columns([1, 1])

    with age_col1:
        head_age = st.number_input(
            "Your age", min_value=0, max_value=100, value=35, step=1, key="head_age"
        )

    # If married, show spouse age input, otherwise show empty column
    with age_col2:
        spouse_age = None
        if is_married:
            spouse_age = st.number_input(
                "Spouse's age",
                min_value=0,
                max_value=100,
                value=35,
                step=1,
                key="spouse_age",
            )

    state = st.selectbox("State of residence", STATE_CODES)

    # Add NYC checkbox if NY is selected
    in_nyc = False
    if state == "NY":
        in_nyc = st.checkbox("I live in New York City")

    num_children = st.number_input(
        "Number of Children", min_value=0, max_value=10, value=0, step=1
    )

    # Inputs for child ages
    child_ages = []
    if num_children > 0:
        st.write("Enter children's ages:")
        for i in range(0, num_children, 6):
            # Create up to 3 columns per row
            cols = st.columns(min(6, num_children - i))
            for j, col in enumerate(cols):
                if i + j < num_children:  # Make sure we don't exceed num_children
                    with col:
                        age = st.number_input(
                            f"Child {i+j+1}",
                            min_value=0,
                            max_value=18,
                            value=5,
                            key=f"child_{i+j}",
                        )
                        child_ages.append(age)

    return is_married, state, child_ages, head_age, spouse_age, in_nyc


def render_import_expenses():
    st.markdown("### Expenses on Imported Goods")

    import_col1, import_col2 = st.columns([1, 1])

    with import_col1:
        china_imports = st.number_input(
            "Annual spending on imported goods from China",
            min_value=0,
            max_value=1000000,
            value=0,
            step=100,
            format="%d",
            help="Estimated annual spending on goods imported from China",
        )

    with import_col2:
        other_imports = st.number_input(
            "Annual spending on imported goods from other countries",
            min_value=0,
            max_value=1000000,
            value=0,
            step=100,
            format="%d",
            help="Estimated annual spending on goods imported from countries other than China",
        )

    return china_imports, other_imports


def render_income_inputs(is_married=False):
    col1, col2 = st.columns([1, 1])

    with col1:
        income = st.number_input(
            "Total wages and salaries excluding overtime and tips",
            min_value=0,
            max_value=10000000,
            value=50000,
            step=500,
            format="%d",
            key="primary_wages",
        )

        social_security = st.number_input(
            "Social Security benefits received by seniors",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            format="%d",
        )

    with col2:
        overtime_income = st.number_input(
            "Overtime income",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            format="%d",
        )

        tip_income = st.number_input(
            "Tip income",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            format="%d",
        )

    # Add collapsible section for capital gains and investment income
    show_investment = st.expander("Capital Gains & Investment Income", expanded=False)

    with show_investment:
        capital_gains = st.number_input(
            "Capital gains",
            min_value=0,
            max_value=10000000,
            value=0,
            step=500,
            format="%d",
        )

        qualified_dividend_income = st.number_input(
            "Qualified dividend income",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            format="%d",
        )

        non_qualified_dividend_income = st.number_input(
            "Non-qualified dividend income",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            format="%d",
        )

        net_investment_income = st.number_input(
            "Net investment income",
            min_value=0,
            max_value=10000000,
            value=0,
            step=500,
            format="%d",
        )

    # Add itemized deductions section below capital gains
    itemized_deductions = render_itemized_deductions()

    return (
        income,
        tip_income,
        overtime_income,
        social_security,
        capital_gains,
        qualified_dividend_income,
        non_qualified_dividend_income,
        net_investment_income,
        itemized_deductions,  # Add this to the return values
    )


def render_itemized_deductions():
    show_itemized = st.expander("Itemized deduction sources", expanded=False)

    with show_itemized:
        medical_expenses = st.number_input(
            "Medical out-of-pocket expenses",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            help="Medical and dental expenses including health insurance premiums, over the counter health expenses, and other medical expenses.",
        )

        real_estate_taxes = st.number_input(
            "Real estate taxes",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            help="Property taxes paid on your primary residence",
        )

        # Split interest inputs into mortgage/investment and auto loan
        mortgage_investment_interest = st.number_input(
            "Mortgage and investment interest",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            help="Mortgage interest and investment interest expenses",
        )

        auto_loan_interest = st.number_input(
            "Auto loan interest",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            help="Interest paid on auto loans",
        )

        # Combine the interest expenses
        total_interest_expense = mortgage_investment_interest + auto_loan_interest

        charitable_cash = st.number_input(
            "Charitable cash donations",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            help="Cash donations to qualified charitable organizations",
        )

        charitable_non_cash = st.number_input(
            "Charitable non-cash donations",
            min_value=0,
            max_value=100000,
            value=0,
            step=500,
            help="Value of donated items like clothing, furniture, etc.",
        )

        qualified_business_income = st.number_input(
            "Qualified business income",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            help="Income from partnerships, S corporations, or sole proprietorships which is eligible for the Qualified Business Income deduction",
        )

        casualty_loss = st.number_input(
            "Casualty loss",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            help="Losses from federally declared disasters",
        )

    return {
        "medical_expenses": medical_expenses,
        "real_estate_taxes": real_estate_taxes,
        "interest_expense": total_interest_expense,
        "auto_loan_interest": auto_loan_interest,
        "charitable_cash": charitable_cash,
        "charitable_non_cash": charitable_non_cash,
        "qualified_business_income": qualified_business_income,
        "casualty_loss": casualty_loss,
    }

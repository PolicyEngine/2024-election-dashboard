import streamlit as st
from utils import STATE_CODES


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

    return is_married, state, child_ages, head_age, spouse_age


def render_income_inputs(is_married=False):
    """
    Render income input fields with optional spouse income if married
    
    Args:
        is_married (bool): Whether the user is married
        
    Returns:
        tuple: (income, social_security, capital_gains, spouse_income)
    """
    col1, col2 = st.columns(2)

    with col1:
        income = st.number_input(
            "Wages and salaries ($)",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            format="%d",
            key="primary_wages"
        )

        capital_gains = st.number_input(
            "Capital gains ($)",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            format="%d",
        )

    with col2:
        # Show spouse income input if married, otherwise empty space
        spouse_income = 0
        if is_married:
            spouse_income = st.number_input(
                "Spouse wages and salaries ($)",
                min_value=0,
                max_value=1000000,
                value=0,
                step=500,
                format="%d",
                key="spouse_wages"
            )
        else:
            st.empty()  # Placeholder to maintain alignment

        social_security = st.number_input(
            "Social security Benefits received by seniors ($)",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            format="%d",
        )

    return income, social_security, capital_gains, spouse_income

def render_itemized_deductions():
    show_itemized = st.expander("Itemized deduction sources", expanded=False)

    with show_itemized:
        medical_expenses = st.number_input(
            "Medical out-of-pocket expenses ($)",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            help="Medical and dental expenses including health insurance premiums, over the counter health expenses, and other medical expenses.",
        )

        real_estate_taxes = st.number_input(
            "Real estate taxes ($)",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            help="Property taxes paid on your primary residence",
        )

        interest_expense = st.number_input(
            "Interest expense ($)",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            help="Mortgage interest and investment interest expenses",
        )

        charitable_cash = st.number_input(
            "Charitable cash donations ($)",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            help="Cash donations to qualified charitable organizations",
        )

        charitable_non_cash = st.number_input(
            "Charitable non-cash donations ($)",
            min_value=0,
            max_value=100000,
            value=0,
            step=500,
            help="Value of donated items like clothing, furniture, etc.",
        )

        qualified_business_income = st.number_input(
            "Qualified business income ($)",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            help="Income from partnerships, S corporations, or sole proprietorships which is eligible for the Qualified Business Income deduction",
        )

        casualty_loss = st.number_input(
            "Casualty loss ($)",
            min_value=0,
            max_value=1000000,
            value=0,
            step=500,
            help="Losses from federally declared disasters",
        )

    return {
        "medical_expenses": medical_expenses,
        "real_estate_taxes": real_estate_taxes,
        "interest_expense": interest_expense,
        "charitable_cash": charitable_cash,
        "charitable_non_cash": charitable_non_cash,
        "qualified_business_income": qualified_business_income,
        "casualty_loss": casualty_loss,
    }

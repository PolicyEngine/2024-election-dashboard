from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from reforms import COMBINED_REFORMS
from policyengine_us.variables.gov.irs.credits.income_tax_refundable_credits import (
    income_tax_refundable_credits as IncomeTaxRefundableCredits,
)
from policyengine_us.variables.gov.states.tax.income.state_refundable_credits import (
    state_refundable_credits as StateRefundableCredits,
)
from policyengine_us.variables.household.income.household.household_benefits import (
    household_benefits as HouseholdBenefits,
)
from utils import YEAR, CHINA_TARIFF_RATE, OTHER_TARIFF_RATE, EITCS, CTCS
import pkg_resources
import yaml
import pandas as pd


def load_credits_from_yaml(package, resource_path):
    yaml_file = pkg_resources.resource_stream(package, resource_path)
    data = yaml.safe_load(yaml_file)
    newest_year = max(data["values"].keys())
    credits = data["values"].get(newest_year, [])
    return credits


def create_situation(
    state,
    is_married,
    child_ages,
    income,
    social_security,
    head_age,
    spouse_age=None,
    medical_expenses=0,
    real_estate_taxes=0,
    interest_expense=0,
    charitable_cash=0,
    charitable_non_cash=0,
    qualified_business_income=0,
    casualty_loss=0,
    capital_gains=0,
    qualified_dividend_income=0,
    non_qualified_dividend_income=0,
    taxable_interest_income=0,
    tip_income=0,
    rental_income=0,
    overtime_income=0,
    in_nyc=False,
):
    # Calculate total employment income
    total_employment_income = income + tip_income + overtime_income

    situation = {
        "people": {
            "you": {
                "age": {YEAR: head_age},
                "employment_income": {YEAR: total_employment_income},
                "social_security": {YEAR: social_security},
                "medical_out_of_pocket_expenses": {YEAR: medical_expenses},
                "interest_expense": {YEAR: interest_expense},
                "charitable_cash_donations": {YEAR: charitable_cash},
                "charitable_non_cash_donations": {YEAR: charitable_non_cash},
                "qualified_business_income": {YEAR: qualified_business_income},
                "casualty_loss": {YEAR: casualty_loss},
                "real_estate_taxes": {YEAR: real_estate_taxes},
                "capital_gains": {YEAR: capital_gains},
                "qualified_dividend_income": {YEAR: qualified_dividend_income},
                "non_qualified_dividend_income": {YEAR: non_qualified_dividend_income},
                "tip_income": {YEAR: tip_income},
                "overtime_income": {YEAR: overtime_income},
                "taxable_interest_income": {YEAR: taxable_interest_income},
                "rental_income": {YEAR: rental_income},
            }
        },
        "tax_units": {
            "your tax unit": {
                "members": ["you"],
            }
        },
        "families": {"family": {"members": ["you"]}},
        "marital_units": {"your marital unit": {"members": ["you"]}},
        "spm_units": {"your household": {"members": ["you"]}},
        "households": {
            "your household": {
                "members": ["you"],
                "state_code": {YEAR: state},
                "in_nyc": {YEAR: in_nyc},
            }
        },
    }

    # Add children if any
    for i, age in enumerate(child_ages):
        child_id = f"child_{i}"
        situation["people"][child_id] = {"age": {YEAR: age}}
        for unit in [
            "families",
            "marital_units",
            "tax_units",
            "households",
            "spm_units",
        ]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append(child_id)

    if is_married and spouse_age is not None:
        situation["people"]["your spouse"] = {
            "age": {YEAR: spouse_age},
        }
        for unit in [
            "families",
            "marital_units",
            "tax_units",
            "households",
            "spm_units",
        ]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append(
                "your spouse"
            )

    return situation


def calculate_values(categories, simulation, year):
    """Helper function to calculate values for a list of categories"""
    result_dict = {}
    for category in categories:
        try:
            amount = int(
                round(simulation.calculate(category, year, map_to="household")[0])
            )
            result_dict[category] = amount
        except:
            result_dict[category] = 0
    return result_dict


def calculate_tariffs(reform_name, china_imports, other_imports):
    """Calculate tariffs based on the reform"""
    if reform_name == "Trump":
        china_tariff = (
            china_imports * CHINA_TARIFF_RATE
        )  # 60% tariff on Chinese imports
        other_tariff = other_imports * OTHER_TARIFF_RATE  # 10% tariff on other imports
        return china_tariff + other_tariff
    return 0


def calculate_consolidated_results(
    reform_name,
    state,
    is_married,
    child_ages,
    income,
    social_security,
    head_age,
    spouse_age=None,
    medical_expenses=0,
    real_estate_taxes=0,
    interest_expense=0,
    auto_loan_interest=0,
    charitable_cash=0,
    charitable_non_cash=0,
    qualified_business_income=0,
    casualty_loss=0,
    capital_gains=0,
    qualified_dividend_income=0,
    non_qualified_dividend_income=0,
    taxable_interest_income=0,
    rental_income=0,
    tip_income=0,
    overtime_income=0,
    china_imports=0,
    other_imports=0,
    in_nyc=False,
):
    # Add auto loan interest to total interest only for Trump reform
    total_interest = interest_expense + (
        auto_loan_interest if reform_name == "Trump" else 0
    )

    # Create situation with updated parameters
    situation = create_situation(
        state,
        is_married,
        child_ages,
        income,
        social_security,
        head_age,
        spouse_age,
        medical_expenses,
        real_estate_taxes,
        total_interest,
        charitable_cash,
        charitable_non_cash,
        qualified_business_income,
        casualty_loss,
        capital_gains,
        qualified_dividend_income,
        non_qualified_dividend_income,
        taxable_interest_income,
        rental_income,
        tip_income,
        overtime_income,
        in_nyc,
    )

    # Create simulation based on reform
    if reform_name == "Baseline":
        simulation = Simulation(situation=situation)
    else:
        reform_dict = COMBINED_REFORMS.get(reform_name, {})
        if not reform_dict:
            simulation = Simulation(situation=situation)
        else:
            reform = Reform.from_dict(reform_dict, country_id="us")
            simulation = Simulation(reform=reform, situation=situation)

    # Calculate federal credits
    package = "policyengine_us"
    resource_path_federal = "parameters/gov/irs/credits/refundable.yaml"
    resource_path_state = (
        f"parameters/gov/states/{state.lower()}/tax/income/credits/refundable.yaml"
    )

    try:
        federal_refundable_credits = load_credits_from_yaml(
            package, resource_path_federal
        )
    except FileNotFoundError:
        federal_refundable_credits = []

    federal_credits_dict = {}
    for credit in federal_refundable_credits:
        try:
            value = int(round(simulation.calculate(credit, YEAR)[0]))
            if value != 0:
                federal_credits_dict[credit] = value
        except:
            continue

    # Calculate specific federal credits
    specific_federal_credits = {
        "refundable_ctc": int(round(simulation.calculate("refundable_ctc", YEAR)[0])),
        "eitc": int(round(simulation.calculate("eitc", YEAR)[0])),
    }
    federal_credits_dict.update(specific_federal_credits)

    # Calculate state-specific credits
    state_code = state.lower()
    state_specific_programs = {
        program for program in (CTCS + EITCS) if program.startswith(f"{state_code}_")
    }

    state_credits_dict = {}
    # First calculate from YAML
    try:
        state_refundable_credits = load_credits_from_yaml(package, resource_path_state)
        for credit in state_refundable_credits:
            try:
                value = int(round(simulation.calculate(credit, YEAR)[0]))
                if value != 0:
                    state_credits_dict[credit] = value
            except:
                continue
    except FileNotFoundError:
        pass

    # Then add state-specific programs
    for program in state_specific_programs:
        try:
            value = int(round(simulation.calculate(program, YEAR)[0]))
            if value != 0:
                state_credits_dict[program] = value
        except:
            continue

    # Calculate benefits
    benefits = [
        "social_security",
        "ssi",
        "snap",
        "wic",
        "free_school_meals",
        "reduced_price_school_meals",
        "spm_unit_broadband_subsidy",
        "tanf",
        "high_efficiency_electric_home_rebate",
        "residential_efficiency_electrification_rebate",
        "unemployment_compensation",
        "head_start",
        "early_head_start",
        "housing_vouchers",
        "medicaid",
        "medicare",
    ]

    benefits_dict = {}
    for benefit in benefits:
        try:
            amount = int(round(simulation.calculate(benefit, YEAR)[0]))
            if amount > 0:
                benefits_dict[benefit] = amount
        except:
            continue

    total_benefits = sum(benefits_dict.values())

    # Calculate tax components
    tax_components = {
        "employee_payroll_tax": int(
            round(simulation.calculate("employee_payroll_tax", YEAR)[0])
        ),
        "income_tax_before_refundable_credits": int(
            round(simulation.calculate("income_tax_before_refundable_credits", YEAR)[0])
        ),
        "household_state_tax_before_refundable_credits": int(
            round(
                simulation.calculate(
                    "household_state_tax_before_refundable_credits", YEAR
                )[0]
            )
        ),
    }

    # Calculate tariffs
    tariffs = calculate_tariffs(reform_name, china_imports, other_imports)
    tariff_components = {
        "china_tariffs": (
            china_imports * CHINA_TARIFF_RATE if reform_name == "Trump" else 0
        ),
        "other_tariffs": (
            other_imports * OTHER_TARIFF_RATE if reform_name == "Trump" else 0
        ),
        "total_tariffs": tariffs,
    }

    # Calculate final income
    household_net_income = int(
        round(simulation.calculate("household_net_income", YEAR)[0])
    )
    adjusted_net_income = max(household_net_income - tariffs, 0)

    # Combine all results
    all_results = {
        "Household Net Income": adjusted_net_income,
        "Household Market Income": int(
            round(simulation.calculate("household_market_income", YEAR)[0])
        ),
        "Income Tax Before Credits": int(
            round(
                simulation.calculate("household_tax_before_refundable_credits", YEAR)[0]
            )
        ),
        "Tariffs": tariffs,
        "Federal Refundable Credits": int(
            round(simulation.calculate("income_tax_refundable_credits", YEAR)[0])
        ),
        "State Refundable Credits": int(
            round(simulation.calculate("state_refundable_credits", YEAR)[0])
        ),
        "Total Benefits": total_benefits,
        **tax_components,
        **benefits_dict,
        **federal_credits_dict,
        **state_credits_dict,
        **tariff_components,
        **specific_federal_credits,
    }

    return pd.DataFrame({reform_name: all_results}).T

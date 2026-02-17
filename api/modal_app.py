"""
Modal API backend for the 2024 Election Dashboard.
Runs PolicyEngine US microsimulations for Baseline, Harris, and Trump tax plans.
"""

import modal

app = modal.App("election-dashboard")

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        "fastapi[standard]",
        "policyengine-us==1.88.0",
        "flask==3.1.0",
        "flask-cors==5.0.0",
        "gunicorn==23.0.0",
        "pyyaml",
    )
)

COMBINED_REFORMS = {
    "Baseline": None,
    "Harris": {
        "gov.contrib.congress.delauro.american_family_act.baby_bonus": {
            "2024-01-01.2100-12-31": 2400
        },
        "gov.irs.credits.ctc.amount.arpa[0].amount": {
            "2023-01-01.2028-12-31": 3600
        },
        "gov.irs.credits.ctc.amount.arpa[1].amount": {
            "2023-01-01.2028-12-31": 3000
        },
        "gov.irs.credits.ctc.phase_out.arpa.in_effect": {
            "2023-01-01.2028-12-31": True
        },
        "gov.irs.credits.ctc.refundable.fully_refundable": {
            "2023-01-01.2028-12-31": True
        },
        "gov.contrib.biden.budget_2025.medicare.rate": {
            "2025-01-01.2100-12-31": 0.012
        },
        "gov.contrib.biden.budget_2025.medicare.threshold": {
            "2025-01-01.2025-12-31": 411000,
        },
        "gov.contrib.biden.budget_2025.net_investment_income.rate": {
            "2025-01-01.2100-12-31": 0.012
        },
        "gov.contrib.biden.budget_2025.net_investment_income.threshold": {
            "2025-01-01.2025-12-31": 411000,
        },
        "gov.irs.income.bracket.rates.7": {
            "2025-01-01.2025-12-31": 0.396
        },
        "gov.irs.income.bracket.thresholds.5.HEAD_OF_HOUSEHOLD": {
            "2026-01-01.2026-12-31": 444600,
        },
        "gov.irs.income.bracket.thresholds.5.JOINT": {
            "2025-01-01.2025-12-31": 462400,
        },
        "gov.irs.income.bracket.thresholds.5.SEPARATE": {
            "2025-01-01.2025-12-31": 231200,
        },
        "gov.irs.income.bracket.thresholds.5.SINGLE": {
            "2026-01-01.2026-12-31": 418450,
        },
        "gov.irs.income.bracket.thresholds.5.SURVIVING_SPOUSE": {
            "2025-01-01.2025-12-31": 462400,
        },
        "gov.irs.credits.eitc.eligibility.age.max": {
            "2024-01-01.2033-12-31": 100
        },
        "gov.irs.credits.eitc.eligibility.age.min": {
            "2024-01-01.2033-12-31": 19
        },
        "gov.irs.credits.eitc.eligibility.age.min_student": {
            "2024-01-01.2033-12-31": 24
        },
        "gov.irs.credits.eitc.max[0].amount": {
            "2025-01-01.2025-12-31": 1774,
        },
        "gov.irs.credits.eitc.phase_in_rate[0].amount": {
            "2024-01-01.2033-12-31": 0.153
        },
        "gov.irs.credits.eitc.phase_out.rate[0].amount": {
            "2024-01-01.2033-12-31": 0.153
        },
        "gov.irs.credits.eitc.phase_out.start[0].amount": {
            "2025-01-01.2025-12-31": 13706,
        },
        "gov.contrib.tax_exempt.in_effect": {
            "2025-01-01.2100-12-31": True
        },
        "gov.contrib.tax_exempt.tip_income.income_tax_exempt": {
            "2025-01-01.2100-12-31": True
        },
        "gov.contrib.tax_exempt.tip_income.payroll_tax_exempt": {
            "2025-01-01.2100-12-31": True
        },
    },
    "Trump": {
        "gov.irs.social_security.taxability.rate.additional": {
            "2024-01-01.2100-12-31": 0
        },
        "gov.irs.social_security.taxability.rate.base": {
            "2024-01-01.2100-12-31": 0
        },
        "gov.contrib.tax_exempt.in_effect": {
            "2025-01-01.2100-12-31": True
        },
        "gov.contrib.tax_exempt.overtime.income_tax_exempt": {
            "2025-01-01.2100-12-31": True
        },
        "gov.contrib.tax_exempt.overtime.payroll_tax_exempt": {
            "2025-01-01.2100-12-31": True
        },
        "gov.contrib.tax_exempt.tip_income.income_tax_exempt": {
            "2025-01-01.2100-12-31": True
        },
        "gov.contrib.tax_exempt.tip_income.payroll_tax_exempt": {
            "2025-01-01.2100-12-31": True
        },
    },
}

YEAR = "2025"


def create_situation(
    state,
    is_married,
    child_ages,
    income,
    social_security_retirement,
    head_age,
    spouse_age=None,
    medical_expenses=0,
    real_estate_taxes=0,
    interest_expense=0,
    charitable_cash=0,
    charitable_non_cash=0,
    qualified_business_income=0,
    casualty_loss=0,
    tip_income=0,
    overtime_income=0,
    reform_name="Baseline",
):
    person_dict = {
        "age": {YEAR: head_age},
        "employment_income": {YEAR: income},
        "social_security_retirement": {YEAR: social_security_retirement},
        "medical_out_of_pocket_expenses": {YEAR: medical_expenses},
        "interest_expense": {YEAR: interest_expense},
        "charitable_cash_donations": {YEAR: charitable_cash},
        "charitable_non_cash_donations": {YEAR: charitable_non_cash},
        "qualified_business_income": {YEAR: qualified_business_income},
        "casualty_loss": {YEAR: casualty_loss},
        "real_estate_taxes": {YEAR: real_estate_taxes},
    }

    if reform_name == "Harris":
        person_dict["service_industry_wages"] = {YEAR: tip_income}
    elif reform_name == "Trump":
        person_dict["service_industry_wages"] = {
            YEAR: tip_income + overtime_income
        }

    situation = {
        "people": {"adult": person_dict},
        "families": {"family": {"members": ["adult"]}},
        "marital_units": {"marital_unit": {"members": ["adult"]}},
        "tax_units": {
            "tax_unit": {
                "members": ["adult"],
                "premium_tax_credit": {YEAR: 0},
                "alternative_minimum_tax": {YEAR: 0},
                "net_investment_income_tax": {YEAR: 0},
            }
        },
        "households": {
            "household": {
                "members": ["adult"],
                "state_code": {YEAR: state},
            }
        },
        "spm_units": {"household": {"members": ["adult"]}},
    }

    for i, age in enumerate(child_ages):
        child_id = f"child_{i}"
        situation["people"][child_id] = {"age": {YEAR: age}}
        for unit in [
            "families",
            "tax_units",
            "households",
            "spm_units",
        ]:
            key = list(situation[unit].keys())[0]
            situation[unit][key]["members"].append(child_id)

    if is_married and spouse_age is not None:
        spouse_dict = {
            "age": {YEAR: spouse_age},
            "employment_income": {YEAR: 0},
        }
        if reform_name in ("Harris", "Trump"):
            spouse_dict["service_industry_wages"] = {YEAR: 0}

        situation["people"]["spouse"] = spouse_dict
        for unit in [
            "families",
            "marital_units",
            "tax_units",
            "households",
            "spm_units",
        ]:
            key = list(situation[unit].keys())[0]
            situation[unit][key]["members"].append("spouse")

    return situation


def calculate_values(categories, simulation, year):
    result_dict = {}
    for category in categories:
        try:
            amount = float(
                simulation.calculate(category, year, map_to="household")[0]
            )
            result_dict[category] = amount
        except Exception:
            result_dict[category] = 0.0
    return result_dict


def run_simulation(reform_name, inputs):
    from policyengine_us import Simulation
    from policyengine_core.reforms import Reform
    import pkg_resources
    import yaml

    state = inputs["state"]
    is_married = inputs["is_married"]
    child_ages = inputs.get("child_ages", [])
    income = inputs.get("income", 0)
    social_security_retirement = inputs.get("social_security_retirement", 0)
    head_age = inputs.get("head_age", 35)
    spouse_age = inputs.get("spouse_age", None)
    tip_income = inputs.get("tip_income", 0)
    overtime_income = inputs.get("overtime_income", 0)
    medical_expenses = inputs.get("medical_expenses", 0)
    real_estate_taxes = inputs.get("real_estate_taxes", 0)
    interest_expense = inputs.get("interest_expense", 0)
    charitable_cash = inputs.get("charitable_cash", 0)
    charitable_non_cash = inputs.get("charitable_non_cash", 0)
    qualified_business_income = inputs.get("qualified_business_income", 0)
    casualty_loss = inputs.get("casualty_loss", 0)

    # Adjust incomes based on reform
    if reform_name == "Baseline":
        total_income = income + tip_income + overtime_income
        tip_income = 0
        overtime_income = 0
    else:
        total_income = income
        if reform_name == "Harris":
            total_income += overtime_income
            overtime_income = 0

    situation = create_situation(
        state=state,
        is_married=is_married,
        child_ages=child_ages,
        income=total_income,
        social_security_retirement=social_security_retirement,
        head_age=head_age,
        spouse_age=spouse_age,
        medical_expenses=medical_expenses,
        real_estate_taxes=real_estate_taxes,
        interest_expense=interest_expense,
        charitable_cash=charitable_cash,
        charitable_non_cash=charitable_non_cash,
        qualified_business_income=qualified_business_income,
        casualty_loss=casualty_loss,
        tip_income=tip_income,
        overtime_income=overtime_income,
        reform_name=reform_name,
    )

    if reform_name == "Baseline":
        simulation = Simulation(situation=situation)
    else:
        reform_dict = COMBINED_REFORMS.get(reform_name, {})
        reform = Reform.from_dict(reform_dict, country_id="us")
        simulation = Simulation(reform=reform, situation=situation)

    household_net_income = float(
        simulation.calculate("household_net_income", YEAR)[0]
    )
    household_refundable_tax_credits = float(
        simulation.calculate("household_refundable_tax_credits", YEAR)[0]
    )
    household_tax_before_refundable_credits = float(
        simulation.calculate(
            "household_tax_before_refundable_credits", YEAR
        )[0]
    )

    # Load credit categories
    package = "policyengine_us"
    resource_path_federal = "parameters/gov/irs/credits/refundable.yaml"
    resource_path_state = (
        f"parameters/gov/states/{state.lower()}/tax/income/credits/"
        f"refundable.yaml"
    )

    def load_credits_from_yaml(pkg, path):
        yaml_file = pkg_resources.resource_stream(pkg, path)
        data = yaml.safe_load(yaml_file)
        newest_year = max(data["values"].keys())
        return data["values"].get(newest_year, [])

    try:
        federal_credits = load_credits_from_yaml(
            package, resource_path_federal
        )
    except FileNotFoundError:
        federal_credits = []

    try:
        state_credits = load_credits_from_yaml(package, resource_path_state)
    except FileNotFoundError:
        state_credits = []

    federal_credits_dict = calculate_values(
        federal_credits, simulation, YEAR
    )
    state_credits_dict = calculate_values(state_credits, simulation, YEAR)

    return {
        "Household Net Income": household_net_income,
        "Income Tax Before Credits": household_tax_before_refundable_credits,
        "Refundable Tax Credits": household_refundable_tax_credits,
        **federal_credits_dict,
        **state_credits_dict,
    }


@app.function(image=image, timeout=300)
@modal.web_endpoint(method="POST")
def calculate(data: dict):
    from flask import jsonify

    inputs = data.get("inputs", {})
    reforms = ["Baseline", "Harris", "Trump"]

    results = {}
    for reform_name in reforms:
        results[reform_name] = run_simulation(reform_name, inputs)

    return {"results": results}


@app.function(image=image, timeout=60)
@modal.web_endpoint(method="GET")
def health():
    return {"status": "ok", "app": "election-dashboard"}

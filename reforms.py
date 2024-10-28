COMBINED_REFORMS = {
    "Baseline": None,
    "Harris": {
        # Harris Child Tax Credit
        "gov.contrib.congress.delauro.american_family_act.baby_bonus": {
            "2024-01-01.2100-12-31": 2400
        },
        "gov.irs.credits.ctc.amount.arpa[0].amount": {"2023-01-01.2028-12-31": 3600},
        "gov.irs.credits.ctc.amount.arpa[1].amount": {"2023-01-01.2028-12-31": 3000},
        "gov.irs.credits.ctc.phase_out.arpa.in_effect": {"2023-01-01.2028-12-31": True},
        "gov.irs.credits.ctc.refundable.fully_refundable": {
            "2023-01-01.2028-12-31": True
        },
        # High Earners Reform
        "gov.contrib.biden.budget_2025.medicare.rate": {"2025-01-01.2100-12-31": 0.012},
        "gov.contrib.biden.budget_2025.medicare.threshold": {
            "2025-01-01.2025-12-31": 411000,
        },
        "gov.contrib.biden.budget_2025.net_investment_income.rate": {
            "2025-01-01.2100-12-31": 0.012
        },
        "gov.contrib.biden.budget_2025.net_investment_income.threshold": {
            "2025-01-01.2025-12-31": 411000,
        },
        "gov.irs.income.bracket.rates.7": {"2025-01-01.2025-12-31": 0.396},
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
        # Capital Gains Reform
        "gov.contrib.harris.capital_gains.in_effect": {"2025-01-01.2100-12-31": True},
        "gov.contrib.harris.capital_gains.brackets.thresholds.3.SEPARATE": {
            "2025-01-01.2100-12-31": 500000
        },
        # Restoring ARPA EITC
        "gov.irs.credits.eitc.eligibility.age.max": {"2024-01-01.2033-12-31": 100},
        "gov.irs.credits.eitc.eligibility.age.min": {"2024-01-01.2033-12-31": 19},
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
        # Tip Income Tax Exemption
        "gov.contrib.tax_exempt.in_effect": {
            "2024-01-01.2100-12-31": True
        },
        "gov.contrib.tax_exempt.tip_income.income_tax_exempt": {
            "2024-01-01.2100-12-31": True
        },
        "gov.contrib.tax_exempt.tip_income.payroll_tax_exempt": {
            "2024-01-01.2100-12-31": False
        },
    },
    "Trump": {
        # Trump Social Security Tax Exemption
        "gov.irs.social_security.taxability.rate.additional": {
            "2024-01-01.2100-12-31": 0
        },
        "gov.irs.social_security.taxability.rate.base": {"2024-01-01.2100-12-31": 0},
        # Trump Tax Exemptions
        "gov.contrib.tax_exempt.in_effect": {
            "2024-01-01.2100-12-31": True
        },
        "gov.contrib.tax_exempt.overtime.income_tax_exempt": {
            "2024-01-01.2100-12-31": True
        },
        "gov.contrib.tax_exempt.overtime.payroll_tax_exempt": {
            "2024-01-01.2100-12-31": True
        },
        "gov.contrib.tax_exempt.tip_income.income_tax_exempt": {
            "2024-01-01.2100-12-31": True
        },
        "gov.contrib.tax_exempt.tip_income.payroll_tax_exempt": {
            "2024-01-01.2100-12-31": False
        }
    }
}

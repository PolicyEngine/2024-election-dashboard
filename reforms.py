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
        # High Earners Reform with inflation adjustments
        "gov.contrib.biden.budget_2025.medicare.rate": {
            "2025-01-01.2100-12-31": 0.012
        },
        "gov.contrib.biden.budget_2025.medicare.threshold": {
            "2025-01-01.2025-12-31": 411000,
            "2026-01-01.2026-12-31": 418450,
            "2027-01-01.2027-12-31": 427500,
            "2028-01-01.2028-12-31": 435950,
        },
        "gov.contrib.biden.budget_2025.net_investment_income.rate": {
            "2025-01-01.2100-12-31": 0.012
        },
        "gov.contrib.biden.budget_2025.net_investment_income.threshold": {
            "2025-01-01.2025-12-31": 411000,
            "2026-01-01.2026-12-31": 418450,
            "2027-01-01.2027-12-31": 427500,
            "2028-01-01.2028-12-31": 435950,
        },
        # Income tax bracket thresholds
        "gov.irs.income.bracket.rates.7": {
            "2025-01-01.2025-12-31": 0.396
        },
        "gov.irs.income.bracket.thresholds.5.HEAD_OF_HOUSEHOLD": {
            "2026-01-01.2026-12-31": 444600,
            "2027-01-01.2027-12-31": 454225,
            "2028-01-01.2028-12-31": 463200,
        },
        "gov.irs.income.bracket.thresholds.5.JOINT": {
            "2025-01-01.2025-12-31": 462400,
            "2026-01-01.2026-12-31": 470750,
            "2027-01-01.2027-12-31": 480950,
            "2028-01-01.2028-12-31": 490450,
        },
        "gov.irs.income.bracket.thresholds.5.SEPARATE": {
            "2025-01-01.2025-12-31": 231200,
            "2026-01-01.2026-12-31": 235375,
            "2027-01-01.2027-12-31": 240475,
            "2028-01-01.2028-12-31": 245225,
        },
        "gov.irs.income.bracket.thresholds.5.SINGLE": {
            "2026-01-01.2026-12-31": 418450,
            "2027-01-01.2027-12-31": 427500,
            "2028-01-01.2028-12-31": 435950,
        },
        "gov.irs.income.bracket.thresholds.5.SURVIVING_SPOUSE": {
            "2025-01-01.2025-12-31": 462400,
            "2026-01-01.2026-12-31": 470750,
            "2027-01-01.2027-12-31": 480950,
            "2028-01-01.2028-12-31": 490450,
        },
        # Additional high-income thresholds
        "gov.irs.income.bracket.thresholds.6.HEAD_OF_HOUSEHOLD": {
            "2025-01-01.2025-12-31": 436700,
            "2026-01-01.2026-12-31": 444600,
            "2027-01-01.2027-12-31": 454225,
            "2028-01-01.2028-12-31": 463200,
        },
        "gov.irs.income.bracket.thresholds.6.JOINT": {
            "2025-01-01.2025-12-31": 462400,
            "2026-01-01.2026-12-31": 470750,
            "2027-01-01.2027-12-31": 480950,
            "2028-01-01.2028-12-31": 490450,
        },
        "gov.irs.income.bracket.thresholds.6.SEPARATE": {
            "2025-01-01.2025-12-31": 231200,
            "2026-01-01.2026-12-31": 235375,
            "2027-01-01.2027-12-31": 240475,
            "2028-01-01.2028-12-31": 245225,
        },
        "gov.irs.income.bracket.thresholds.6.SINGLE": {
            "2025-01-01.2025-12-31": 411000,
            "2026-01-01.2026-12-31": 418450,
            "2027-01-01.2027-12-31": 427500,
            "2028-01-01.2028-12-31": 435950,
        },
        "gov.irs.income.bracket.thresholds.6.SURVIVING_SPOUSE": {
            "2025-01-01.2025-12-31": 462400,
            "2026-01-01.2026-12-31": 470750,
            "2027-01-01.2027-12-31": 480950,
            "2028-01-01.2028-12-31": 490450,
        },

        # Capital Gains Reform
        "gov.contrib.harris.capital_gains.in_effect": {
            "2024-01-01.2100-12-31": True
        },
        "gov.contrib.harris.capital_gains.brackets.thresholds.3.SEPARATE": {
            "2025-01-01.2025-12-31": 500000,
        },
        # Capital Gains Reform
        "gov.contrib.harris.capital_gains.in_effect": {"2024-01-01.2100-12-31": True},
        "gov.contrib.harris.capital_gains.brackets.thresholds.3.SEPARATE": {
            "2024-01-01.2100-12-31": 500000
        },
        # Restoring ARPA EITC
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
            "2024-01-01.2024-12-31": 1756,
            "2025-01-01.2025-12-31": 1774,
            "2026-01-01.2026-12-31": 1815,
            "2027-01-01.2027-12-31": 1852,
            "2028-01-01.2028-12-31": 1888,
        },
        "gov.irs.credits.eitc.phase_in_rate[0].amount": {
            "2024-01-01.2033-12-31": 0.153
        },
        "gov.irs.credits.eitc.phase_out.rate[0].amount": {
            "2024-01-01.2033-12-31": 0.153
        },
        "gov.irs.credits.eitc.phase_out.start[0].amount": {
            "2024-01-01.2024-12-31": 13565,
            "2025-01-01.2025-12-31": 13706,
            "2026-01-01.2026-12-31": 14022,
            "2027-01-01.2027-12-31": 14306,
            "2028-01-01.2028-12-31": 14582,
        },
    },
    "Trump": {
        # Social Security Tax Exemption
        "gov.irs.social_security.taxability.rate.additional": {
            "2024-01-01.2100-12-31": 0
        },
        "gov.irs.social_security.taxability.rate.base": {
            "2024-01-01.2100-12-31": 0
        },
        
        # Tax Brackets and Rates
        "gov.irs.income.bracket.rates.2": {"2026-01-01.2100-12-31": 0.12},
        "gov.irs.income.bracket.rates.3": {"2026-01-01.2100-12-31": 0.22},
        "gov.irs.income.bracket.rates.4": {"2026-01-01.2100-12-31": 0.24},
        "gov.irs.income.bracket.rates.5": {"2026-01-01.2100-12-31": 0.32},
        "gov.irs.income.bracket.rates.7": {"2026-01-01.2100-12-31": 0.37},
        
        # Child Tax Credit
        "gov.irs.credits.ctc.amount.adult_dependent": {
            "2026-01-01.2100-12-31": 500
        },
        "gov.irs.credits.ctc.amount.base[0].amount": {
            "2026-01-01.2100-12-31": 2000
        },
        "gov.irs.credits.ctc.phase_out.threshold.HEAD_OF_HOUSEHOLD": {
            "2026-01-01.2100-12-31": 200000
        },
        "gov.irs.credits.ctc.phase_out.threshold.JOINT": {
            "2026-01-01.2100-12-31": 400000
        },
        "gov.irs.credits.ctc.phase_out.threshold.SEPARATE": {
            "2026-01-01.2100-12-31": 200000
        },
        "gov.irs.credits.ctc.phase_out.threshold.SINGLE": {
            "2026-01-01.2100-12-31": 200000
        },
        "gov.irs.credits.ctc.phase_out.threshold.SURVIVING_SPOUSE": {
            "2026-01-01.2100-12-31": 400000
        },
        
        # CTC Refundability
        "gov.irs.credits.ctc.refundable.individual_max": {
            "2026-01-01.2026-12-31": 1800,
            "2027-01-01.2027-12-31": 1800,
            "2028-01-01.2028-12-31": 1800,
            "2029-01-01.2029-12-31": 1900,
            "2030-01-01.2030-12-31": 1900,
            "2031-01-01.2031-12-31": 1900,
            "2032-01-01.2032-12-31": 2000,
            "2033-01-01.2033-12-31": 2000,
            "2034-01-01.2034-12-31": 2000,
            "2035-01-01.2035-12-31": 2000
        },
        "gov.irs.credits.ctc.refundable.phase_in.threshold": {
            "2026-01-01.2100-12-31": 2500
        },
        
        # Itemized Deductions
        "gov.irs.deductions.itemized.casualty.active": {
            "2026-01-01.2100-12-31": False
        },
        "gov.irs.deductions.itemized.charity.ceiling.all": {
            "2026-01-01.2100-12-31": 0.6
        },
        "gov.irs.deductions.itemized.limitation.agi_rate": {
            "2026-01-01.2100-12-31": None
        },
        "gov.irs.deductions.itemized.limitation.itemized_deduction_rate": {
            "2026-01-01.2100-12-31": None
        },
        
        # SALT Cap
        "gov.irs.deductions.itemized.salt_and_real_estate.cap.HEAD_OF_HOUSEHOLD": {
            "2026-01-01.2100-12-31": 10000
        },
        "gov.irs.deductions.itemized.salt_and_real_estate.cap.JOINT": {
            "2026-01-01.2100-12-31": 10000
        },
        "gov.irs.deductions.itemized.salt_and_real_estate.cap.SEPARATE": {
            "2026-01-01.2100-12-31": 5000
        },
        "gov.irs.deductions.itemized.salt_and_real_estate.cap.SINGLE": {
            "2026-01-01.2100-12-31": 10000
        },
        "gov.irs.deductions.itemized.salt_and_real_estate.cap.SURVIVING_SPOUSE": {
            "2026-01-01.2100-12-31": 10000
        },
        
        # Standard Deduction (with inflation adjustments)
        "gov.irs.deductions.standard.amount.HEAD_OF_HOUSEHOLD": {
            "2026-01-01.2026-12-31": 22950,
            "2027-01-01.2027-12-31": 23425,
            "2028-01-01.2028-12-31": 23875
        },
        "gov.irs.deductions.standard.amount.JOINT": {
            "2026-01-01.2026-12-31": 30600,
            "2027-01-01.2027-12-31": 31225,
            "2028-01-01.2028-12-31": 31825
        },
        
        # Personal Exemption
        "gov.irs.income.exemption.amount": {
            "2026-01-01.2100-12-31": 0
        }
    }
}
REFORMS = {
    "Baseline": None,
    "Harris LIFT Middle Class Tax Credit": {
        "gov.contrib.harris.lift.middle_class_tax_credit.in_effect": {
            "2024-01-01.2100-12-31": True
        }
    },
    "Harris Rent Relief Act": {
        "gov.contrib.harris.rent_relief_act.rent_relief_credit.in_effect": {
            "2024-01-01.2100-12-31": True
        }
    },
    "Vance Current Refundability CTC": {
        "gov.irs.credits.ctc.amount.base[0].amount": {
            "2024-01-01.2100-12-31": 5000
        },
        "gov.irs.credits.ctc.phase_out.amount": {
            "2024-01-01.2100-12-31": 0
        }
    },
    "Vance Refundable CTC": {
        "gov.irs.credits.ctc.amount.base[0].amount": {
            "2024-01-01.2100-12-31": 5000
        },
        "gov.irs.credits.ctc.phase_out.amount": {
            "2024-01-01.2100-12-31": 0
        },
        "gov.irs.credits.ctc.refundable.fully_refundable": {
            "2024-01-01.2100-12-31": True
        }
    },
    "Harris CTC": {
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
        }
    }
}
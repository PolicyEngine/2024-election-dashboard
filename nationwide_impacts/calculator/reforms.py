import numpy as np

# Child Tax Credit Reform
CTC_REFORM = {
    "gov.contrib.congress.delauro.american_family_act.baby_bonus": {
        "2024-01-01.2100-12-31": 2400
    },
    "gov.irs.credits.ctc.amount.arpa[0].amount": {"2023-01-01.2028-12-31": 3600},
    "gov.irs.credits.ctc.amount.arpa[1].amount": {"2023-01-01.2028-12-31": 3000},
    "gov.irs.credits.ctc.phase_out.arpa.in_effect": {"2023-01-01.2028-12-31": True},
    "gov.irs.credits.ctc.refundable.fully_refundable": {"2023-01-01.2028-12-31": True},
}


# EITC Reform
EITC_REFORM = {
    "gov.irs.credits.eitc.eligibility.age.max": {"2024-01-01.2033-12-31": 100},
    "gov.irs.credits.eitc.eligibility.age.min": {"2024-01-01.2033-12-31": 19},
    "gov.irs.credits.eitc.eligibility.age.min_student": {"2024-01-01.2033-12-31": 24},
    "gov.irs.credits.eitc.max[0].amount": {
        "2025-01-01.2025-12-31": 1774,
    },
    "gov.irs.credits.eitc.phase_in_rate[0].amount": {"2024-01-01.2033-12-31": 0.153},
    "gov.irs.credits.eitc.phase_out.rate[0].amount": {"2024-01-01.2033-12-31": 0.153},
    "gov.irs.credits.eitc.phase_out.start[0].amount": {
        "2025-01-01.2025-12-31": 13706,
    },
}

# Social Security Reform
SOCIAL_SECURITY_REFORM = {
    "gov.irs.social_security.taxability.rate.additional": {"2024-01-01.2100-12-31": 0},
    "gov.irs.social_security.taxability.rate.base": {"2024-01-01.2100-12-31": 0},
}


# SALT Cap Reform
SALT_CAP_REFORM = {
    "gov.irs.deductions.itemized.salt_and_real_estate.cap.HEAD_OF_HOUSEHOLD": {
        "2025-01-01.2100-12-31": np.inf
    },
    "gov.irs.deductions.itemized.salt_and_real_estate.cap.JOINT": {
        "2025-01-01.2100-12-31": np.inf
    },
    "gov.irs.deductions.itemized.salt_and_real_estate.cap.SEPARATE": {
        "2025-01-01.2100-12-31": np.inf
    },
    "gov.irs.deductions.itemized.salt_and_real_estate.cap.SINGLE": {
        "2025-01-01.2100-12-31": np.inf
    },
    "gov.irs.deductions.itemized.salt_and_real_estate.cap.SURVIVING_SPOUSE": {
        "2025-01-01.2100-12-31": np.inf
    },
}

# Combined dictionary for all reforms
REFORMS = {
    "Baseline": None,
    "Harris CTC Reform": CTC_REFORM,
    "Harris EITC Reform": EITC_REFORM,
    "Trump Social Security Reform": SOCIAL_SECURITY_REFORM,
    "Trump SALT Cap Reform": SALT_CAP_REFORM,
}

export interface HouseholdInputs {
  state: string;
  is_married: boolean;
  child_ages: number[];
  head_age: number;
  spouse_age: number | null;
  income: number;
  social_security_retirement: number;
  tip_income: number;
  overtime_income: number;
  medical_expenses: number;
  real_estate_taxes: number;
  interest_expense: number;
  charitable_cash: number;
  charitable_non_cash: number;
  qualified_business_income: number;
  casualty_loss: number;
}

export interface ReformResults {
  "Household Net Income": number;
  "Income Tax Before Credits": number;
  "Refundable Tax Credits": number;
  [creditName: string]: number;
}

export interface CalculationResponse {
  results: {
    Baseline: ReformResults;
    Harris: ReformResults;
    Trump: ReformResults;
  };
}

export type ReformName = "Baseline" | "Harris" | "Trump";

export const MAIN_METRICS = [
  "Household Net Income",
  "Income Tax Before Credits",
  "Refundable Tax Credits",
] as const;

export const STATE_CODES = [
  "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL",
  "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME",
  "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH",
  "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI",
  "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI",
  "WY",
] as const;

export const STATE_NAMES: Record<string, string> = {
  AL: "Alabama", AK: "Alaska", AZ: "Arizona", AR: "Arkansas",
  CA: "California", CO: "Colorado", CT: "Connecticut",
  DC: "District of Columbia", DE: "Delaware", FL: "Florida",
  GA: "Georgia", HI: "Hawaii", ID: "Idaho", IL: "Illinois",
  IN: "Indiana", IA: "Iowa", KS: "Kansas", KY: "Kentucky",
  LA: "Louisiana", ME: "Maine", MD: "Maryland", MA: "Massachusetts",
  MI: "Michigan", MN: "Minnesota", MS: "Mississippi", MO: "Missouri",
  MT: "Montana", NE: "Nebraska", NV: "Nevada", NH: "New Hampshire",
  NJ: "New Jersey", NM: "New Mexico", NY: "New York",
  NC: "North Carolina", ND: "North Dakota", OH: "Ohio",
  OK: "Oklahoma", OR: "Oregon", PA: "Pennsylvania",
  RI: "Rhode Island", SC: "South Carolina", SD: "South Dakota",
  TN: "Tennessee", TX: "Texas", UT: "Utah", VT: "Vermont",
  VA: "Virginia", WA: "Washington", WV: "West Virginia",
  WI: "Wisconsin", WY: "Wyoming",
};

export const DEFAULT_INPUTS: HouseholdInputs = {
  state: "CA",
  is_married: false,
  child_ages: [],
  head_age: 35,
  spouse_age: null,
  income: 30000,
  social_security_retirement: 0,
  tip_income: 0,
  overtime_income: 0,
  medical_expenses: 0,
  real_estate_taxes: 0,
  interest_expense: 0,
  charitable_cash: 0,
  charitable_non_cash: 0,
  qualified_business_income: 0,
  casualty_loss: 0,
};

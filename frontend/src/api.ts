import type { HouseholdInputs, CalculationResponse } from "./types";

const API_URL =
  import.meta.env.VITE_API_URL ||
  "https://policyengine--election-dashboard-calculate.modal.run";

export async function calculateHouseholdImpact(
  inputs: HouseholdInputs,
): Promise<CalculationResponse> {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ inputs }),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

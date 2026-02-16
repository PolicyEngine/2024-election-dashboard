import { render, screen } from "@testing-library/react";
import { MantineProvider } from "@mantine/core";
import { describe, it, expect } from "vitest";
import { CreditsTable } from "../components/CreditsTable";

describe("CreditsTable", () => {
  it("shows message when no active credits", () => {
    const results = {
      Baseline: {
        "Household Net Income": 25000,
        "Income Tax Before Credits": 3000,
        "Refundable Tax Credits": 1000,
      },
      Harris: {
        "Household Net Income": 27000,
        "Income Tax Before Credits": 2500,
        "Refundable Tax Credits": 1500,
      },
      Trump: {
        "Household Net Income": 26000,
        "Income Tax Before Credits": 2800,
        "Refundable Tax Credits": 1200,
      },
    };
    render(
      <MantineProvider>
        <CreditsTable results={results} stateCode="CA" />
      </MantineProvider>,
    );
    expect(
      screen.getByText(/no changes in credit components/i),
    ).toBeInTheDocument();
  });

  it("renders active credit rows", () => {
    const results = {
      Baseline: {
        "Household Net Income": 25000,
        "Income Tax Before Credits": 3000,
        "Refundable Tax Credits": 1000,
        eitc: 500,
      },
      Harris: {
        "Household Net Income": 27000,
        "Income Tax Before Credits": 2500,
        "Refundable Tax Credits": 1500,
        eitc: 1200,
      },
      Trump: {
        "Household Net Income": 26000,
        "Income Tax Before Credits": 2800,
        "Refundable Tax Credits": 1200,
        eitc: 500,
      },
    };
    render(
      <MantineProvider>
        <CreditsTable results={results} stateCode="CA" />
      </MantineProvider>,
    );
    expect(screen.getByText("EITC")).toBeInTheDocument();
  });
});

import { render, screen } from "@testing-library/react";
import { MantineProvider } from "@mantine/core";
import { describe, it, expect } from "vitest";
import { NetIncomeChart } from "../components/NetIncomeChart";

const mockResults = {
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

describe("NetIncomeChart", () => {
  it("renders the chart title", () => {
    render(
      <MantineProvider>
        <NetIncomeChart results={mockResults} />
      </MantineProvider>,
    );
    expect(
      screen.getByText(/household net income comparison/i),
    ).toBeInTheDocument();
  });
});

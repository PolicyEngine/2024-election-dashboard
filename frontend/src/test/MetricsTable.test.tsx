import { render, screen } from "@testing-library/react";
import { MantineProvider } from "@mantine/core";
import { describe, it, expect } from "vitest";
import { MetricsTable } from "../components/MetricsTable";

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

describe("MetricsTable", () => {
  it("renders all main metric rows", () => {
    render(
      <MantineProvider>
        <MetricsTable results={mockResults} />
      </MantineProvider>,
    );
    expect(screen.getByText("Household Net Income")).toBeInTheDocument();
    expect(screen.getByText("Income Tax Before Credits")).toBeInTheDocument();
    expect(screen.getByText("Refundable Tax Credits")).toBeInTheDocument();
  });

  it("renders column headers", () => {
    render(
      <MantineProvider>
        <MetricsTable results={mockResults} />
      </MantineProvider>,
    );
    expect(screen.getByText("Baseline")).toBeInTheDocument();
    expect(screen.getByText("Harris")).toBeInTheDocument();
    expect(screen.getByText("Trump")).toBeInTheDocument();
  });

  it("renders formatted currency values", () => {
    render(
      <MantineProvider>
        <MetricsTable results={mockResults} />
      </MantineProvider>,
    );
    expect(screen.getByText("$25,000.00")).toBeInTheDocument();
    expect(screen.getByText("$27,000.00")).toBeInTheDocument();
  });
});

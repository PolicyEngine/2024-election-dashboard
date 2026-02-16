import { render, screen } from "@testing-library/react";
import { MantineProvider } from "@mantine/core";
import { describe, it, expect } from "vitest";
import App from "../App";

function renderWithProviders(ui: React.ReactElement) {
  return render(<MantineProvider>{ui}</MantineProvider>);
}

describe("App", () => {
  it("renders the title", () => {
    renderWithProviders(<App />);
    expect(
      screen.getByText(
        /2024 election, personal household impact calculator/i,
      ),
    ).toBeInTheDocument();
  });

  it("renders the calculate button", () => {
    renderWithProviders(<App />);
    expect(
      screen.getByRole("button", { name: /calculate my household income/i }),
    ).toBeInTheDocument();
  });

  it("renders personal information section", () => {
    renderWithProviders(<App />);
    expect(screen.getByText(/personal information/i)).toBeInTheDocument();
  });

  it("renders income information section", () => {
    renderWithProviders(<App />);
    expect(screen.getByText(/income information/i)).toBeInTheDocument();
  });

  it("does not show results before calculation", () => {
    renderWithProviders(<App />);
    expect(
      screen.queryByText(/household net income comparison/i),
    ).not.toBeInTheDocument();
  });
});

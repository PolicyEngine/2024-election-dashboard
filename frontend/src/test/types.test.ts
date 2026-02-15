import { describe, it, expect } from "vitest";
import {
  STATE_CODES,
  STATE_NAMES,
  DEFAULT_INPUTS,
  MAIN_METRICS,
} from "../types";

describe("types and constants", () => {
  it("has 51 state codes (50 states + DC)", () => {
    expect(STATE_CODES).toHaveLength(51);
  });

  it("has matching state names for all codes", () => {
    for (const code of STATE_CODES) {
      expect(STATE_NAMES[code]).toBeDefined();
    }
  });

  it("has correct default inputs", () => {
    expect(DEFAULT_INPUTS.state).toBe("CA");
    expect(DEFAULT_INPUTS.is_married).toBe(false);
    expect(DEFAULT_INPUTS.child_ages).toEqual([]);
    expect(DEFAULT_INPUTS.income).toBe(30000);
    expect(DEFAULT_INPUTS.head_age).toBe(35);
  });

  it("has three main metrics", () => {
    expect(MAIN_METRICS).toHaveLength(3);
    expect(MAIN_METRICS).toContain("Household Net Income");
    expect(MAIN_METRICS).toContain("Income Tax Before Credits");
    expect(MAIN_METRICS).toContain("Refundable Tax Credits");
  });
});

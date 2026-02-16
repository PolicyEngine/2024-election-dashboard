import {
  Stack,
  Title,
  Slider,
  NumberInput,
  Accordion,
  Text,
  Box,
} from "@mantine/core";
import type { HouseholdInputs } from "../types";

interface Props {
  inputs: HouseholdInputs;
  onChange: (updates: Partial<HouseholdInputs>) => void;
}

function formatCurrency(value: number): string {
  return `$${value.toLocaleString()}`;
}

function IncomeSlider({
  label,
  value,
  max,
  step,
  helpText,
  onChange,
}: {
  label: string;
  value: number;
  max: number;
  step: number;
  helpText?: string;
  onChange: (val: number) => void;
}) {
  return (
    <Box>
      <Text size="sm" fw={500} mb={4}>
        {label}: {formatCurrency(value)}
      </Text>
      {helpText && (
        <Text size="xs" c="dimmed" mb={4}>
          {helpText}
        </Text>
      )}
      <Slider
        value={value}
        onChange={onChange}
        min={0}
        max={max}
        step={step}
        label={formatCurrency}
      />
    </Box>
  );
}

export function IncomeForm({ inputs, onChange }: Props) {
  return (
    <Stack gap="md">
      <Title order={3}>Income information</Title>

      <IncomeSlider
        label="Annual wages and salaries"
        value={inputs.income}
        max={500000}
        step={500}
        helpText="Regular wages and salaries (excluding overtime and tips)"
        onChange={(val) => onChange({ income: val })}
      />

      <IncomeSlider
        label="Annual social security retirement income"
        value={inputs.social_security_retirement}
        max={500000}
        step={500}
        onChange={(val) => onChange({ social_security_retirement: val })}
      />

      <IncomeSlider
        label="Annual tip income"
        value={inputs.tip_income}
        max={100000}
        step={100}
        helpText="Total annual income from tips"
        onChange={(val) => onChange({ tip_income: val })}
      />

      <IncomeSlider
        label="Annual overtime income"
        value={inputs.overtime_income}
        max={100000}
        step={100}
        helpText="Total annual income from overtime work"
        onChange={(val) => onChange({ overtime_income: val })}
      />

      <Accordion>
        <Accordion.Item value="itemized">
          <Accordion.Control>Itemized deduction sources</Accordion.Control>
          <Accordion.Panel>
            <Stack gap="sm">
              <NumberInput
                label="Medical out-of-pocket expenses ($)"
                description="Medical and dental expenses that exceed 7.5% of your AGI"
                min={0}
                max={1000000}
                step={500}
                value={inputs.medical_expenses}
                onChange={(val) =>
                  onChange({
                    medical_expenses: typeof val === "number" ? val : 0,
                  })
                }
              />
              <NumberInput
                label="Real estate taxes ($)"
                description="Property taxes paid on your primary residence"
                min={0}
                max={1000000}
                step={500}
                value={inputs.real_estate_taxes}
                onChange={(val) =>
                  onChange({
                    real_estate_taxes: typeof val === "number" ? val : 0,
                  })
                }
              />
              <NumberInput
                label="Interest expense ($)"
                description="Mortgage interest and investment interest expenses"
                min={0}
                max={1000000}
                step={500}
                value={inputs.interest_expense}
                onChange={(val) =>
                  onChange({
                    interest_expense: typeof val === "number" ? val : 0,
                  })
                }
              />
              <NumberInput
                label="Charitable cash donations ($)"
                description="Cash donations to qualified charitable organizations"
                min={0}
                max={1000000}
                step={500}
                value={inputs.charitable_cash}
                onChange={(val) =>
                  onChange({
                    charitable_cash: typeof val === "number" ? val : 0,
                  })
                }
              />
              <NumberInput
                label="Charitable non-cash donations ($)"
                description="Value of donated items like clothing, furniture, etc."
                min={0}
                max={100000}
                step={500}
                value={inputs.charitable_non_cash}
                onChange={(val) =>
                  onChange({
                    charitable_non_cash: typeof val === "number" ? val : 0,
                  })
                }
              />
              <NumberInput
                label="Qualified business income ($)"
                description="Income from partnerships, S corporations, or sole proprietorships"
                min={0}
                max={1000000}
                step={500}
                value={inputs.qualified_business_income}
                onChange={(val) =>
                  onChange({
                    qualified_business_income:
                      typeof val === "number" ? val : 0,
                  })
                }
              />
              <NumberInput
                label="Casualty loss ($)"
                description="Losses from federally declared disasters"
                min={0}
                max={1000000}
                step={500}
                value={inputs.casualty_loss}
                onChange={(val) =>
                  onChange({
                    casualty_loss: typeof val === "number" ? val : 0,
                  })
                }
              />
            </Stack>
          </Accordion.Panel>
        </Accordion.Item>
      </Accordion>
    </Stack>
  );
}

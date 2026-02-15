import {
  Stack,
  Title,
  Checkbox,
  NumberInput,
  Select,
  Grid,
  Group,
  Text,
} from "@mantine/core";
import type { HouseholdInputs } from "../types";
import { STATE_CODES, STATE_NAMES } from "../types";

interface Props {
  inputs: HouseholdInputs;
  onChange: (updates: Partial<HouseholdInputs>) => void;
}

const stateOptions = STATE_CODES.map((code) => ({
  value: code,
  label: `${code} - ${STATE_NAMES[code]}`,
}));

export function PersonalInfoForm({ inputs, onChange }: Props) {
  return (
    <Stack gap="md">
      <Title order={3}>Personal information</Title>

      <Checkbox
        label="I am married"
        checked={inputs.is_married}
        onChange={(e) => {
          const married = e.currentTarget.checked;
          onChange({
            is_married: married,
            spouse_age: married ? 35 : null,
          });
        }}
      />

      <Grid>
        <Grid.Col span={inputs.is_married ? 6 : 12}>
          <NumberInput
            label="Your age"
            min={0}
            max={100}
            value={inputs.head_age}
            onChange={(val) =>
              onChange({ head_age: typeof val === "number" ? val : 35 })
            }
          />
        </Grid.Col>
        {inputs.is_married && (
          <Grid.Col span={6}>
            <NumberInput
              label="Spouse's age"
              min={0}
              max={100}
              value={inputs.spouse_age ?? 35}
              onChange={(val) =>
                onChange({
                  spouse_age: typeof val === "number" ? val : 35,
                })
              }
            />
          </Grid.Col>
        )}
      </Grid>

      <Select
        label="State of residence"
        data={stateOptions}
        value={inputs.state}
        onChange={(val) => onChange({ state: val ?? "CA" })}
        searchable
      />

      <NumberInput
        label="Number of children"
        min={0}
        max={10}
        value={inputs.child_ages.length}
        onChange={(val) => {
          const count = typeof val === "number" ? val : 0;
          const current = inputs.child_ages;
          if (count > current.length) {
            const newAges = [
              ...current,
              ...Array(count - current.length).fill(5),
            ];
            onChange({ child_ages: newAges });
          } else {
            onChange({ child_ages: current.slice(0, count) });
          }
        }}
      />

      {inputs.child_ages.length > 0 && (
        <Stack gap="xs">
          <Text size="sm" fw={500}>
            Children's ages:
          </Text>
          <Group gap="sm">
            {inputs.child_ages.map((age, i) => (
              <NumberInput
                key={i}
                label={`Child ${i + 1}`}
                min={0}
                max={18}
                value={age}
                w={100}
                onChange={(val) => {
                  const newAges = [...inputs.child_ages];
                  newAges[i] = typeof val === "number" ? val : 5;
                  onChange({ child_ages: newAges });
                }}
              />
            ))}
          </Group>
        </Stack>
      )}
    </Stack>
  );
}

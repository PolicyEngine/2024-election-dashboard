import { useState, useCallback } from "react";
import {
  Container,
  Title,
  Text,
  Button,
  Stack,
  Grid,
  Tabs,
  Alert,
  Anchor,
  Loader,
  Center,
} from "@mantine/core";
import type {
  HouseholdInputs,
  CalculationResponse,
} from "./types";
import { DEFAULT_INPUTS } from "./types";
import { calculateHouseholdImpact } from "./api";
import { PersonalInfoForm } from "./components/PersonalInfoForm";
import { IncomeForm } from "./components/IncomeForm";
import { NetIncomeChart } from "./components/NetIncomeChart";
import { MetricsTable } from "./components/MetricsTable";
import { CreditsTable } from "./components/CreditsTable";
import { ReformDetails } from "./components/ReformDetails";

export default function App() {
  const [inputs, setInputs] = useState<HouseholdInputs>(DEFAULT_INPUTS);
  const [results, setResults] = useState<CalculationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCalculate = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await calculateHouseholdImpact(inputs);
      setResults(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "An unexpected error occurred",
      );
    } finally {
      setLoading(false);
    }
  }, [inputs]);

  const updateInputs = useCallback(
    (updates: Partial<HouseholdInputs>) => {
      setInputs((prev) => ({ ...prev, ...updates }));
    },
    [],
  );

  return (
    <Container size="lg" py="xl">
      <Stack gap="lg">
        <Title order={1}>
          2024 Election, personal household impact calculator
        </Title>

        <Text>
          This calculator compares how tax proposals from the two major party
          presidential candidates would affect your household's net income.
          Enter your household information below to see a personalized analysis
          of each plan's impact.
        </Text>

        <Text size="sm">
          <strong>Learn more:</strong>{" "}
          <Anchor
            href="https://kamalaharris.com/wp-content/uploads/2024/09/Policy_Book_Economic-Opportunity.pdf"
            target="_blank"
            rel="noopener noreferrer"
          >
            Harris economic policy document
          </Anchor>
          {" | "}
          <Anchor
            href="https://rncplatform.donaldjtrump.com/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Trump campaign platform
          </Anchor>
        </Text>

        <Title order={2}>Enter your current household information</Title>

        <Grid>
          <Grid.Col span={{ base: 12, md: 6 }}>
            <PersonalInfoForm inputs={inputs} onChange={updateInputs} />
          </Grid.Col>
          <Grid.Col span={{ base: 12, md: 6 }}>
            <IncomeForm inputs={inputs} onChange={updateInputs} />
          </Grid.Col>
        </Grid>

        <Button
          size="lg"
          onClick={handleCalculate}
          loading={loading}
          fullWidth
        >
          Calculate my household income
        </Button>

        {error && (
          <Alert color="red" title="Calculation error">
            {error}
          </Alert>
        )}

        {loading && !results && (
          <Center py="xl">
            <Stack align="center" gap="md">
              <Loader size="lg" />
              <Text c="dimmed">
                Running simulations for Baseline, Harris, and Trump plans...
              </Text>
            </Stack>
          </Center>
        )}

        {results && (
          <Stack gap="lg">
            <NetIncomeChart results={results.results} />

            <ReformDetails />

            <Tabs defaultValue="main">
              <Tabs.List>
                <Tabs.Tab value="main">Main breakdown</Tabs.Tab>
                <Tabs.Tab value="credits">Refundable credits</Tabs.Tab>
              </Tabs.List>

              <Tabs.Panel value="main" pt="md">
                <MetricsTable results={results.results} />
              </Tabs.Panel>

              <Tabs.Panel value="credits" pt="md">
                <CreditsTable
                  results={results.results}
                  stateCode={inputs.state}
                />
              </Tabs.Panel>
            </Tabs>

            <Text size="sm" c="dimmed">
              <strong>Assumptions and notes:</strong> All calculations are
              based on projected 2025 tax parameters. The calculator assumes
              all income is from employment (wages and salaries). Whether to
              use standard or itemized deductions is calculated based on the
              user input. The calculator uses the PolicyEngine US
              microsimulation model. Actual impacts may vary based on
              individual circumstances and final policy implementations.
            </Text>
          </Stack>
        )}
      </Stack>
    </Container>
  );
}

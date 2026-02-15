import { Stack, Title, Text, List, Anchor, Paper } from "@mantine/core";

export function ReformDetails() {
  return (
    <Stack gap="md">
      <Title order={2}>Reform details</Title>

      <Paper p="md" withBorder>
        <Title order={3} mb="sm">
          Harris economic package
        </Title>
        <List spacing="xs">
          <List.Item>
            <strong>Enhanced child tax credit:</strong> Restoring the 2021
            expansion with full refundability and a $2,400 "baby bonus".{" "}
            <Anchor
              href="https://policyengine.org/us/research/harris-ctc"
              target="_blank"
              rel="noopener noreferrer"
              size="sm"
            >
              Learn more
            </Anchor>
          </List.Item>
          <List.Item>
            <strong>High earners reform:</strong> Adjustments to tax rates and
            thresholds for high-income earners
          </List.Item>
          <List.Item>
            <strong>Restored EITC:</strong> Bringing back the expanded American
            Rescue Plan version of the earned income tax credit
          </List.Item>
          <List.Item>
            <strong>Tip income tax relief:</strong> Exempting tip income from
            both income and payroll taxes
          </List.Item>
        </List>
      </Paper>

      <Paper p="md" withBorder>
        <Title order={3} mb="sm">
          Trump economic package
        </Title>
        <List spacing="xs">
          <List.Item>
            <strong>Social security tax exemption:</strong> Eliminating taxes on
            social security benefits.{" "}
            <Anchor
              href="https://policyengine.org/us/research/social-security-tax-exemption"
              target="_blank"
              rel="noopener noreferrer"
              size="sm"
            >
              Learn more
            </Anchor>
          </List.Item>
          <List.Item>
            <strong>Tip income tax relief:</strong> Exempting all tip income
            from both income and payroll taxes
          </List.Item>
          <List.Item>
            <strong>Overtime tax relief:</strong> Exempting all overtime income
            from both income and payroll taxes
          </List.Item>
        </List>
      </Paper>

      <Text size="sm" c="dimmed">
        This calculator compares the economic proposals of the two major party
        tickets in the 2024 presidential election.
      </Text>
    </Stack>
  );
}

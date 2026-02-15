import { Table, Text } from "@mantine/core";
import type { ReformResults } from "../types";
import { MAIN_METRICS, STATE_NAMES } from "../types";

interface Props {
  results: {
    Baseline: ReformResults;
    Harris: ReformResults;
    Trump: ReformResults;
  };
  stateCode: string;
}

function formatCurrency(value: number): string {
  return `$${value.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}

const CREDIT_ACRONYMS: Record<string, string> = {
  eitc: "EITC",
  ctc: "CTC",
};

function formatCreditName(name: string, stateCode: string): string {
  let formatted = name.replace("tax_unit_", "");
  const stateName = STATE_NAMES[stateCode] ?? stateCode;
  formatted = formatted.replace(/state_name/gi, stateName);
  formatted = formatted.replace(/_/g, " ");
  formatted = formatted.replace(/\b\w/g, (c) => c.toUpperCase());
  for (const [lower, upper] of Object.entries(CREDIT_ACRONYMS)) {
    const titleCase = lower.charAt(0).toUpperCase() + lower.slice(1);
    formatted = formatted.replace(new RegExp(titleCase, "g"), upper);
  }
  return formatted;
}

export function CreditsTable({ results, stateCode }: Props) {
  const allKeys = new Set<string>();
  for (const reform of Object.values(results)) {
    for (const key of Object.keys(reform)) {
      if (
        !MAIN_METRICS.includes(
          key as (typeof MAIN_METRICS)[number],
        )
      ) {
        allKeys.add(key);
      }
    }
  }

  const activeCredits = [...allKeys].filter((key) => {
    return Object.values(results).some((r) => (r[key] ?? 0) !== 0);
  });

  if (activeCredits.length === 0) {
    return <Text c="dimmed">No changes in credit components</Text>;
  }

  return (
    <Table striped highlightOnHover>
      <Table.Thead>
        <Table.Tr>
          <Table.Th>Credit</Table.Th>
          <Table.Th style={{ textAlign: "right" }}>Baseline</Table.Th>
          <Table.Th style={{ textAlign: "right" }}>Harris</Table.Th>
          <Table.Th style={{ textAlign: "right" }}>Trump</Table.Th>
        </Table.Tr>
      </Table.Thead>
      <Table.Tbody>
        {activeCredits.map((key) => (
          <Table.Tr key={key}>
            <Table.Td>{formatCreditName(key, stateCode)}</Table.Td>
            <Table.Td style={{ textAlign: "right" }}>
              {formatCurrency(results.Baseline[key] ?? 0)}
            </Table.Td>
            <Table.Td style={{ textAlign: "right" }}>
              {formatCurrency(results.Harris[key] ?? 0)}
            </Table.Td>
            <Table.Td style={{ textAlign: "right" }}>
              {formatCurrency(results.Trump[key] ?? 0)}
            </Table.Td>
          </Table.Tr>
        ))}
      </Table.Tbody>
    </Table>
  );
}

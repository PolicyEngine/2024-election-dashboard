import { Table } from "@mantine/core";
import type { ReformResults } from "../types";
import { MAIN_METRICS } from "../types";

interface Props {
  results: {
    Baseline: ReformResults;
    Harris: ReformResults;
    Trump: ReformResults;
  };
}

function formatCurrency(value: number): string {
  return `$${value.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}

export function MetricsTable({ results }: Props) {
  return (
    <Table striped highlightOnHover>
      <Table.Thead>
        <Table.Tr>
          <Table.Th>Metric</Table.Th>
          <Table.Th style={{ textAlign: "right" }}>Baseline</Table.Th>
          <Table.Th style={{ textAlign: "right" }}>Harris</Table.Th>
          <Table.Th style={{ textAlign: "right" }}>Trump</Table.Th>
        </Table.Tr>
      </Table.Thead>
      <Table.Tbody>
        {MAIN_METRICS.map((metric) => (
          <Table.Tr key={metric}>
            <Table.Td>{metric}</Table.Td>
            <Table.Td style={{ textAlign: "right" }}>
              {formatCurrency(results.Baseline[metric])}
            </Table.Td>
            <Table.Td style={{ textAlign: "right" }}>
              {formatCurrency(results.Harris[metric])}
            </Table.Td>
            <Table.Td style={{ textAlign: "right" }}>
              {formatCurrency(results.Trump[metric])}
            </Table.Td>
          </Table.Tr>
        ))}
      </Table.Tbody>
    </Table>
  );
}

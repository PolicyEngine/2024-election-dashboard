import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  LabelList,
} from "recharts";
import { Title, Box } from "@mantine/core";
import type { ReformResults } from "../types";
import { designTokens } from "../designTokens";

interface Props {
  results: {
    Baseline: ReformResults;
    Harris: ReformResults;
    Trump: ReformResults;
  };
}

function formatCurrency(value: number): string {
  return `$${Math.round(value).toLocaleString()}`;
}

const COLORS: Record<string, string> = {
  Baseline: designTokens.colors.baseline,
  Harris: designTokens.colors.harris,
  Trump: designTokens.colors.trump,
};

export function NetIncomeChart({ results }: Props) {
  const baselineIncome = results.Baseline["Household Net Income"];

  const data = [
    {
      name: "Trump",
      value: results.Trump["Household Net Income"],
      diff: results.Trump["Household Net Income"] - baselineIncome,
    },
    {
      name: "Baseline",
      value: baselineIncome,
      diff: 0,
    },
    {
      name: "Harris",
      value: results.Harris["Household Net Income"],
      diff: results.Harris["Household Net Income"] - baselineIncome,
    },
  ].sort((a, b) => a.value - b.value);

  const maxValue = Math.max(...data.map((d) => d.value));

  return (
    <Box>
      <Title order={3} ta="center" mb="md">
        Household net income comparison
      </Title>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 10, right: 120, left: 80, bottom: 10 }}
        >
          <XAxis
            type="number"
            tickFormatter={formatCurrency}
            domain={[0, maxValue * 1.15]}
          />
          <YAxis
            type="category"
            dataKey="name"
            width={70}
            tick={{ fontSize: 14 }}
          />
          <Tooltip
            formatter={(value: number, _name: string, entry) => {
              const diff = (entry.payload as (typeof data)[0]).diff;
              const diffStr =
                diff === 0
                  ? formatCurrency(diff)
                  : diff > 0
                    ? `+${formatCurrency(diff)}`
                    : `-${formatCurrency(Math.abs(diff))}`;
              return [
                `Total: ${formatCurrency(value)} (${diffStr})`,
                "Net income",
              ];
            }}
          />
          <Bar dataKey="value" barSize={40}>
            {data.map((entry) => (
              <Cell
                key={entry.name}
                fill={COLORS[entry.name] ?? designTokens.colors.baseline}
              />
            ))}
            <LabelList
              dataKey="value"
              position="insideRight"
              formatter={formatCurrency}
              style={{ fill: "#fff", fontSize: 13, fontWeight: 500 }}
            />
            <LabelList
              dataKey="diff"
              position="right"
              formatter={(val: number) =>
                val === 0
                  ? ""
                  : val > 0
                    ? `+${formatCurrency(val)}`
                    : `-${formatCurrency(Math.abs(val))}`
              }
              style={{ fontSize: 13, fontWeight: 500 }}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Box>
  );
}

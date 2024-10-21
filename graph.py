import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig
from config import REFORMS

# Function to create the reform comparison graph with formatted colors and bars
def create_reform_comparison_graph(results):
    # Convert the results dictionary into a DataFrame
    df = pd.DataFrame(results.items(), columns=["reform", "net_income"])

    fig = go.Figure()

    # Get the baseline value for comparison
    baseline_value = results.get("Baseline", 0)

    # Create bars for each reform
    for reform, value in zip(df["reform"], df["net_income"]):
        diff = value - baseline_value
        total_text = f"${value:,.0f}"
        diff_text = f"+${diff:,.0f}" if diff > 0 else (f"-${abs(diff):,.0f}" if diff < 0 else "")

        # Bar for the baseline income in grey
        fig.add_trace(go.Bar(
            x=[reform],
            y=[baseline_value],
            name=f"Baseline of {reform}",
            marker_color='grey',
            hoverinfo='none',
            showlegend=False
        ))

        # Bar for the excess portion over the baseline in the respective color
        if reform in REFORMS:
            reform_color = REFORMS[reform].get('color', 'blue')
        else:
            reform_color = 'blue'  # Default color if not found

        fig.add_trace(go.Bar(
            x=[reform],
            y=[diff],
            name=f"Excess of {reform}",
            marker_color=reform_color,
            base=[baseline_value] if diff > 0 else [baseline_value + diff],
            hovertemplate=f"Total: $%{{y:,.0f}}<br>Difference: {diff_text}",
            text=total_text if diff == 0 else "",  # Show the total only for baseline
            showlegend=False
        ))

        # Add annotation for the total value on top of the bar
        fig.add_annotation(
            x=reform,
            y=value,
            text=total_text,
            showarrow=False,
            yshift=10,
            font=dict(size=12),
        )

        # Add annotation for the difference only if not zero
        if diff != 0:
            fig.add_annotation(
                x=reform,
                y=baseline_value + (diff / 2),
                text=diff_text,
                showarrow=False,
                font=dict(size=12, color='white'),
            )

    # Update layout settings
    fig.update_layout(
        title="Net Income Comparison",
        xaxis_title="Reforms",
        yaxis_title="Net Income ($)",
        barmode="stack",
        height=600,
        showlegend=False,
    )

    # Apply the format_fig function for consistent styling
    fig = format_fig(fig)

    return fig

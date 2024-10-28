import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig
from utils import BLUE, RED, GREY, format_currency


def create_reform_comparison_graph(results):
    # Convert the results dictionary into a DataFrame and round values
    df = pd.DataFrame(results.items(), columns=["reform", "net_income"])
    df["net_income"] = df["net_income"].round(0)  # Round to nearest dollar

    # Split baseline and other reforms
    non_baseline = df[df["reform"] != "Baseline"].copy()
    baseline = df[df["reform"] == "Baseline"].copy()

    # Sort non-baseline reforms by net_income (ascending puts larger value at bottom)
    non_baseline = non_baseline.sort_values("net_income", ascending=True)

    # Combine back together with baseline and reverse to get baseline on top
    df = pd.concat([baseline, non_baseline]).iloc[::-1]

    baseline_value = int(round(results.get("Baseline", 0)))  # Force to integer

    fig = go.Figure()

    # Use predefined colors
    colors = {"Baseline": GREY, "Harris": BLUE, "Trump": RED}

    # Create bars
    for reform, value in zip(df["reform"], df["net_income"]):
        value = int(round(value))  # Force to integer
        diff = int(round(value - baseline_value))  # Force to integer
        total_text = f"<b>{format_currency(value)}</b>"  # Bold the total
        diff_text = (
            f"<b>{format_currency(diff)}</b>"  # Show and bold when diff is 0
            if diff == 0
            else (
                f"+<b>{format_currency(diff)}</b>"
                if diff > 0
                else f"-<b>{format_currency(abs(diff))}</b>"
            )
        )

        # Add bar
        fig.add_trace(
            go.Bar(
                y=[reform],
                x=[value],
                orientation="h",
                name=reform,
                marker_color=colors.get(reform, GREY),
                text=total_text,
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(color="white", size=14),
                hovertemplate=(
                    f"Total: {total_text}<br>" f"Difference: {diff_text}<extra></extra>"
                ),
                showlegend=False,
            )
        )

        # Add reform label on the left
        fig.add_annotation(
            y=reform,
            x=0,
            text=reform,
            xanchor="right",
            yanchor="middle",
            xshift=-10,
            showarrow=False,
            font=dict(size=16),
        )

        # Add difference annotation for non-baseline reforms
        if reform != "Baseline":
            annotation_color = colors.get(
                reform, "black"
            )  # Use bar color for annotation
            fig.add_annotation(
                y=reform,
                x=value,
                xanchor="left",
                yanchor="middle",
                xshift=10,
                text=diff_text,
                showarrow=False,
                font=dict(size=16, color=annotation_color),  # Set annotation color
            )

    # Calculate x-axis range
    max_value = df["net_income"].max()
    x_max = max_value * 1.2

    # Basic layout
    fig.update_layout(
        title={
            "text": "Household Net Income Comparison",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(size=32),
        },
        height=400,
        showlegend=False,
        margin=dict(t=70, b=50, l=150, r=150),
        yaxis=dict(showgrid=False, showline=False, showticklabels=False, ticks=""),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            showline=True,
            linecolor="rgba(0,0,0,0.2)",
            tickformat="$,d",  # Changed to remove decimals
            range=[0, x_max],
            title="Household Net Income",
            title_standoff=20,
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        bargap=0.5,
    )

    # Apply PolicyEngine formatting
    fig = format_fig(fig)

    return fig

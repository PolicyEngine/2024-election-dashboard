import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig
from utils import BLUE, RED, GREY, format_currency


def create_reform_comparison_graph(results):
    # Convert the results dictionary into a DataFrame and round values
    df = pd.DataFrame(results.items(), columns=["reform", "net_income"])
    df["net_income"] = df["net_income"].round(0)

    # Sort and reverse to put smallest at top
    df = df.sort_values("net_income", ascending=True).iloc[::-1]

    baseline_value = int(round(results.get("Baseline", 0)))

    fig = go.Figure()

    # Use predefined colors
    colors = {"Baseline": GREY, "Harris": BLUE, "Trump": RED}

    # Create bars
    for reform, value in zip(df["reform"], df["net_income"]):
        value = int(round(value))
        diff = int(round(value - baseline_value))
        text_inside = format_currency(value)
        diff_text = (
            format_currency(diff)
            if diff == 0
            else (
                f"+{format_currency(diff)}"
                if diff > 0
                else f"-{format_currency(abs(diff))}"
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
                text=f"<b>{text_inside}</b>",
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(color="white", size=16, weight="bold"),
                hovertemplate=(
                    f"Total: {text_inside}<br>"
                    f"Difference: {diff_text}<extra></extra>"
                ),
                showlegend=False,
            )
        )

        # Add reform label on the left, setting color to match the bar color
        fig.add_annotation(
            y=reform,
            x=0,
            text=reform,
            xanchor="right",
            yanchor="middle",
            xshift=-10,
            showarrow=False,
            font=dict(size=16, color=colors.get(reform, GREY)),  # Match color
        )

        # Add difference annotation for non-baseline reforms
        if reform != "Baseline":
            annotation_color = colors.get(reform, "black")
            fig.add_annotation(
                y=reform,
                x=value,
                xanchor="left",
                yanchor="middle",
                xshift=10,
                text=f"<b>{diff_text}</b>",
                showarrow=False,
                font=dict(size=14, color=annotation_color),
            )

    # Calculate x-axis range
    max_value = df["net_income"].max()
    x_max = max_value

    # Update layout with mobile-friendly settings and left-aligned title
    fig.update_layout(
        title={
            "text": "<b>How would each candidate's policies affect your net income in 2025?</b>",
            "y": 0.95,
            "x": 0,  # Left align
            "xanchor": "left",  # Left align
            "yanchor": "top",
            "font": dict(size=20),
            "xref": "paper",
            "pad": dict(t=10, b=10, l=0),  # Adjust padding around title
        },
        height=300,  # Reduced height for mobile
        showlegend=False,
        margin=dict(t=80, b=50, r=100, l=120),  # Reduced right margin from 200 to 100
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            ticks="",
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            showline=True,
            linecolor="rgba(0,0,0,0.2)",
            tickformat="$,.0f",
            range=[0, x_max],
            tickfont=dict(size=12),
            title=dict(text="Household Net Income", font=dict(size=14), standoff=15),
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        bargap=0.15,
        font=dict(size=12),
        uniformtext_minsize=8,
        uniformtext_mode="hide",
    )

    # Make the graph responsive
    fig.update_layout(
        autosize=True,
        xaxis=dict(
            automargin=True,
            constrain="domain",
        ),
        yaxis=dict(
            automargin=True,
            constrain="domain",
        ),
    )

    # Apply PolicyEngine formatting
    fig = format_fig(fig)

    # Override the logo settings with larger size
    if len(fig.layout.images) > 0:
        fig.layout.images[0].update(
            sizex=0.15,  # Increased from 0.08
            sizey=0.15,  # Increased from 0.08
            x=1,
            y=-0.1,
            xanchor="right",
            yanchor="bottom"
        )

    return fig
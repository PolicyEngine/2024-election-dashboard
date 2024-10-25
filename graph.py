import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig
from utils import BLUE, RED, GREY, format_currency
 

def create_reform_comparison_graph(results):
    # Convert the results dictionary into a DataFrame
    df = pd.DataFrame(results.items(), columns=["reform", "net_income"])
    
    # Split baseline and other reforms
    non_baseline = df[df["reform"] != "Baseline"].copy()
    baseline = df[df["reform"] == "Baseline"].copy()
    
    # Sort non-baseline reforms by net_income (ascending puts larger value at bottom)
    non_baseline = non_baseline.sort_values("net_income", ascending=True)
    
    # Combine back together with baseline and reverse to get baseline on top
    df = pd.concat([baseline, non_baseline]).iloc[::-1]

    baseline_value = results.get("Baseline", 0)
    
    fig = go.Figure()

    # Use predefined colors
    colors = {
        "Baseline": GREY,
        "Harris": BLUE,
        "Trump": RED
    }

    # Create bars
    for reform, value in zip(df["reform"], df["net_income"]):
        diff = value - baseline_value
        total_text = format_currency(value)
        diff_text = (
            format_currency(diff) if diff == 0 
            else f"+{format_currency(diff)}" if diff > 0 
            else f"-{format_currency(abs(diff))}"
        )
        
        # Add bar
        fig.add_trace(go.Bar(
            y=[reform],
            x=[value],
            orientation='h',
            name=reform,
            marker_color=colors.get(reform, GREY),
            text=total_text,
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(color='white', size=14),
            hovertemplate=(
                f"Total: {total_text}<br>"
                f"Difference: {diff_text}<extra></extra>"
            ),
            showlegend=False
        ))

        # Add reform label on the left
        fig.add_annotation(
            y=reform,
            x=0,
            text=reform,
            xanchor='right',
            yanchor='middle',
            xshift=-10,
            showarrow=False,
            font=dict(size=16)
        )

        # Add difference annotation for non-baseline reforms
        if reform != "Baseline" and diff != 0:
            fig.add_annotation(
                y=reform,
                x=value,
                xanchor='left',
                yanchor='middle',
                xshift=10,
                text=diff_text,
                showarrow=False,
                font=dict(size=16)
            )

    # Calculate x-axis range
    max_value = df['net_income'].max()
    x_max = max_value * 1.2
    
    # Basic layout
    fig.update_layout(
        title={
            'text': "Household Net Income Comparison",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=32)
        },
        height=400,
        showlegend=False,
        margin=dict(t=70, b=50, l=150, r=150),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            ticks=''
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            showline=True,
            linecolor='rgba(0,0,0,0.2)',
            tickformat='$,.0f',
            range=[0, x_max],
            title="Household Net Income",
            title_standoff=20
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        bargap=0.5
    )

    # Apply PolicyEngine formatting
    fig = format_fig(fig)
    
    return fig
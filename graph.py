import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig
from utils import BLUE, RED, GREY

def create_reform_comparison_graph(results):
    # Convert the results dictionary into a DataFrame
    df = pd.DataFrame(results.items(), columns=["reform", "net_income"])
    
    # Sort the reforms: Baseline first, then others by ascending value
    non_baseline = df[df["reform"] != "Baseline"].copy()
    baseline = df[df["reform"] == "Baseline"].copy()
    
    # Sort non-baseline reforms by net_income
    non_baseline = non_baseline.sort_values("net_income", ascending=True)
    
    # Combine back together: Baseline at top, followed by sorted reforms
    df = pd.concat([baseline, non_baseline])
    
    # Reverse the order for display (since bars are built bottom-to-top)
    df = df.iloc[::-1]

    fig = go.Figure()

    # Get the baseline value for comparison
    baseline_value = results.get("Baseline", 0)

    # Create bars for each reform
    for reform, value in zip(df["reform"], df["net_income"]):
        diff = value - baseline_value
        total_text = f"${value:,.0f}"
        diff_text = f"+${diff:,.0f}" if diff > 0 else (f"-${abs(diff):,.0f}" if diff < 0 else "")
        
        # Modify the reform name display
        display_name = reform if reform == "Baseline" else (
            "Harris" if reform == "Harris" else "Trump"
        )

        # Set up bar colors
        if reform == "Baseline":
            color = GREY
        elif reform == "Harris":
            color = BLUE
        else:  # Trump
            color = RED

        # Add the bar without y-axis labels (we'll add them as annotations)
        fig.add_trace(go.Bar(
            y=[reform],
            x=[value],
            name=reform,
            marker_color=color,
            orientation='h',
            text=total_text,
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(
                color='white',
                size=20
            ),
            hovertemplate=f"Total: {total_text}<br>Difference: {diff_text}<extra></extra>",
            showlegend=False
        ))

        # Add custom label on the left
        fig.add_annotation(
            y=reform,
            x=0,
            text=display_name,
            xanchor='right',
            yanchor='middle',
            xshift=-10,  # Offset to the left of the bar
            showarrow=False,
            font=dict(
                size=16,
                color='black'
            ),
        )

        # Add the difference annotation for non-baseline reforms
        if reform != "Baseline" and diff != 0:
            fig.add_annotation(
                y=reform,
                x=value,
                xanchor='left',
                yanchor='middle',
                xshift=10,  # Offset to the right of the bar
                text=diff_text,
                showarrow=False,
                font=dict(
                    size=20,
                    color='black'
                ),
            )

    # Update layout settings
    fig.update_layout(
        title={
            'text': "Household Net Income by Reform",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=32)
        },
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=70, b=30, l=150, r=150),
        yaxis={
            'categoryorder': 'array', 
            'categoryarray': df["reform"].tolist(),  # Use our explicitly sorted order
            'showgrid': False,
            'showline': False,
            'ticks': '',
            'showticklabels': False,  # Hide default y-axis labels
        },
        xaxis={
            'showgrid': False,
            'showline': False,
            'showticklabels': False,
            'ticks': '',
        },
        bargap=0.5
    )

    # Apply the format_fig function for consistent styling
    fig = format_fig(fig)

    return fig
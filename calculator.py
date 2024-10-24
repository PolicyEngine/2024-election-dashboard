import pandas as pd
from results import calculate_consolidated_results
from graph import create_reform_comparison_graph

def calculate_reforms(inputs, progress_text, chart_placeholder):
    summary_results = {}
    results_df = pd.DataFrame(
        index=[
            "Household Net Income",
            "Income Tax Before Credits",
            "Refundable Tax Credits"
        ],
        columns=["Baseline", "Harris", "Trump"],
        dtype=float
    )
    
    reforms_to_calculate = ["Baseline", "Harris", "Trump"]
    
    for reform in reforms_to_calculate:
        progress_text.text(f"Calculating {reform}...")
        # Calculate just this reform
        single_reform_df = calculate_consolidated_results(reform, **inputs)
        
        # Update our results storage
        for idx in results_df.index:
            results_df.at[idx, reform] = single_reform_df.at[idx, reform]
        summary_results[reform] = results_df.at["Household Net Income", reform]
        
        # Update the chart
        fig = create_reform_comparison_graph(summary_results)
        chart_placeholder.plotly_chart(fig, use_container_width=True)
    
    return summary_results, results_df

def format_detailed_metrics(results_df):
    formatted_df = results_df.copy()
    formatted_df = formatted_df.round(2)
    formatted_df = formatted_df.applymap(lambda x: f"${x:,.2f}")
    return formatted_df

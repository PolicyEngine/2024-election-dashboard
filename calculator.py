import pandas as pd
from results import calculate_results, calculate_detailed_metrics
from graph import create_reform_comparison_graph

def calculate_reforms(inputs, progress_text, chart_placeholder):
    results = {}
    reforms_to_calculate = ["Baseline", "Harris", "Trump"]
    
    for reform in reforms_to_calculate:
        progress_text.text(f"Calculating {reform}...")
        reform_results = calculate_results([reform], **inputs)
        results[reform] = reform_results[reform]
        
        # Update the chart after each calculation
        fig = create_reform_comparison_graph(results)
        chart_placeholder.plotly_chart(fig, use_container_width=True)
    
    return results

def format_detailed_metrics(detailed_df):
    formatted_df = pd.DataFrame(
        index=detailed_df.index,
        columns=detailed_df.columns
    )
    
    for idx in detailed_df.index:
        for col in detailed_df.columns:
            value = detailed_df.at[idx, col]
            formatted_df.at[idx, col] = f"${round(value):,}"
    
    return formatted_df
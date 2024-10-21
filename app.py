import streamlit as st
import plotly.graph_objects as go
from policyengine_core.charts import format_fig
from results import calculate_results
from config import REFORMS, APP_TITLE, BASELINE_DESCRIPTION, REFORMS_DESCRIPTION, NOTES
from utils import STATE_CODES
import pandas as pd

st.set_page_config(page_title=APP_TITLE, page_icon="👪", layout="wide")
st.title(APP_TITLE)

st.markdown(BASELINE_DESCRIPTION)

col1, col2 = st.columns(2)

with col1:
    state = st.selectbox("Select State", STATE_CODES)
    num_children = st.number_input("Number of Children", min_value=0, max_value=10, value=2, step=1)

with col2:
    income = st.number_input("Annual Employment Income", min_value=0, max_value=500000, value=50000, step=1000)
    rent = st.number_input("Annual Rent", min_value=0, max_value=120000, value=12000, step=1000)

available_reforms = list(REFORMS.keys())[1:]  # Exclude Baseline
selected_reforms = st.multiselect("Select Reforms to Compare", available_reforms, 
                                  format_func=lambda x: REFORMS[x]['name'])

if st.button("Calculate"):
    results = calculate_results(selected_reforms, state, num_children, income, rent)
    
    # Create DataFrame
    df = pd.DataFrame(columns=["Scenario", "Net Income", "Difference", "Percent Change"])
    baseline_income = results["Baseline"]
    
    for scenario, net_income in results.items():
        difference = net_income - baseline_income
        percent_change = (difference / baseline_income) * 100
        df = df.append({
            "Scenario": scenario,
            "Net Income": net_income,
            "Difference": difference,
            "Percent Change": percent_change
        }, ignore_index=True)
    
    # Display descriptions only for selected reforms
    st.markdown("## Selected Reforms")
    for reform in selected_reforms:
        st.markdown(f"### {REFORMS[reform]['name']}")
        st.markdown(REFORMS[reform]['description'])
        st.markdown(f"[Read full report]({REFORMS[reform]['link']})")
    
    st.markdown("## Results")

    # Plotting
    df_plot = df[df["Scenario"] != "Baseline"]  # Exclude baseline from plot
    fig = go.Figure()

    for _, row in df_plot.iterrows():
        fig.add_trace(go.Bar(
            x=[REFORMS[row["Scenario"]]['name']],
            y=[row["Difference"]],
            name=REFORMS[row["Scenario"]]['name'],
            marker_color=REFORMS[row["Scenario"]]['color']
        ))

    fig.update_layout(
        title=f"Net Income Difference Comparison (Income: ${income:,}, Rent: ${rent:,}/year)",
        xaxis_title="Reforms",
        yaxis_title="Difference in Net Income ($)",
        height=600,
    )

    fig.update_yaxes(tickformat="$,.0f")

    # Add value labels on the bars
    for trace in fig.data:
        y_value = trace.y[0]
        fig.add_annotation(
            x=trace.x[0],
            y=y_value,
            text=f"${y_value:,.0f}",
            showarrow=False,
            yshift=10 if y_value >= 0 else -10,
            font=dict(color="black")
        )

    fig = format_fig(fig)
    st.plotly_chart(fig, use_container_width=True)

    # Formatting the DataFrame for display
    df_display = df.copy()
    df_display["Scenario"] = df_display["Scenario"].map(lambda x: REFORMS[x]['name'])
    df_display["Net Income"] = df_display["Net Income"].apply(lambda x: f"${x:,.2f}")
    df_display["Difference"] = df_display["Difference"].apply(lambda x: f"${x:,.2f}")
    df_display["Percent Change"] = df_display["Percent Change"].apply(lambda x: f"{x:.2f}%")

    st.write("Results Table:")
    st.dataframe(df_display.set_index("Scenario"))

st.markdown(NOTES)
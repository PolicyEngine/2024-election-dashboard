import streamlit as st
import plotly.graph_objects as go
from policyengine_core.charts import format_fig
from results import calculate_results

st.title("2024 Election Household Calculator: Reform Comparisons")

# Define all state codes
STATE_CODES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC"
]

state = st.selectbox("Select State", STATE_CODES)
num_children = st.number_input("Number of Children", min_value=0, max_value=10, value=2, step=1)
income = st.number_input("Annual Employment Income", min_value=0, max_value=500000, value=50000, step=1000)
rent = st.number_input("Annual Rent", min_value=0, max_value=120000, value=12000, step=1000)

available_reforms = [
    "Harris LIFT Middle Class Tax Credit",
    "Harris Rent Relief Act",
    "Harris CTC",
    "Vance Current Refundability CTC",
    "Vance Refundable CTC"
]
selected_reforms = st.multiselect("Select Reforms to Compare", available_reforms)

if st.button("Calculate"):
    df = calculate_results(selected_reforms, state, num_children, income, rent)
    
    # Plotting
    df_plot = df[df["Scenario"] != "Baseline"]  # Exclude baseline from plot
    fig = go.Figure()

    for _, row in df_plot.iterrows():
        fig.add_trace(go.Bar(
            x=[row["Scenario"]],
            y=[row["Difference"]],
            name=row["Scenario"]
        ))

    fig.update_layout(
        title=f"Net Income Difference Comparison (Income: ${income:,}, Rent: ${rent:,}/year)",
        xaxis_title="Reforms",
        yaxis_title="Difference in Net Income ($)",
        height=600,
        width=800,
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
    st.plotly_chart(fig)

    # Formatting the DataFrame for display
    df_display = df.copy()
    df_display["Net Income"] = df_display["Net Income"].apply(lambda x: f"${x:,.2f}")
    df_display["Difference"] = df_display["Difference"].apply(lambda x: f"${x:,.2f}")
    df_display["Percent Change"] = df_display["Percent Change"].apply(lambda x: f"{x:.2f}%")

    st.write("Results:")
    st.dataframe(df_display.set_index("Scenario"))

st.write("Note: This calculator uses PolicyEngine US and simulates the effects of the selected reforms on household net income.")
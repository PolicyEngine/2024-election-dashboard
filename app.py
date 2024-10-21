import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig
from results import calculate_results
from config import REFORMS, APP_TITLE, NOTES
from utils import STATE_CODES, YEAR

st.set_page_config(page_title=APP_TITLE, page_icon="👪", layout="wide")
st.title(APP_TITLE)

col1, col2 = st.columns(2)

with col1:
    is_married = st.checkbox("I am married")
    state = st.selectbox("Select State", STATE_CODES)
    num_children = st.number_input("Number of Children", min_value=0, max_value=10, value=0, step=1)
    
    # Child age inputs
    child_ages = []
    if num_children > 0:
        age_cols = st.columns(min(num_children, 3))  # Up to 3 columns for child ages
        for i in range(num_children):
            with age_cols[i % 3]:
                age = st.number_input(f"Age Child {i+1}", min_value=0, max_value=18, value=5, key=f"child_{i}")
                child_ages.append(age)

with col2:
    income = st.slider("Annual Employment Income", min_value=0, max_value=500000, value=50000, step=1000, format="$%d")
    social_security_retirement = st.slider("Annual Social Security Retirement Income", min_value=0, max_value=50000, value=0, step=100, format="$%d")
    rent = st.slider("Annual Rent", min_value=0, max_value=120000, value=12000, step=100, format="$%d")
    fair_market_rent = st.number_input("Small Area Fair Market Rent (yearly)", min_value=0, max_value=120000, value=12000, step=100)

# Reform selection using checkboxes
st.markdown("## Select Reforms to Compare")
available_reforms = list(REFORMS.keys())[1:]  # Exclude Baseline

# Separate reforms into two groups
harris_walz_reforms = [reform for reform in available_reforms if any(name in reform for name in ['Harris', 'Walz'])]
trump_vance_reforms = [reform for reform in available_reforms if any(name in reform for name in ['Trump', 'Vance'])]

selected_reforms = []
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Harris/Walz Reforms")
    for reform in harris_walz_reforms:
        if st.checkbox(REFORMS[reform]['name'], key=f"reform_{reform}"):
            selected_reforms.append(reform)

with col2:
    st.markdown("### Trump/Vance Reforms")
    for reform in trump_vance_reforms:
        if st.checkbox(REFORMS[reform]['name'], key=f"reform_{reform}"):
            selected_reforms.append(reform)


if st.button("Calculate"):
    # Display descriptions for selected reforms immediately after button press
    if selected_reforms:
        st.markdown("## Selected Reforms")
        for reform in selected_reforms:
            st.markdown(f"### {REFORMS[reform]['name']}")
            st.markdown(REFORMS[reform]['description'])
            if 'link' in REFORMS[reform]:
                st.markdown(f"[Read our full report on this reform.]({REFORMS[reform]['link']})")
    
    # Now trigger the calculations
    results = calculate_results(selected_reforms, state, is_married, child_ages, income, rent, fair_market_rent, social_security_retirement)
    
    # Convert results to DataFrame
    df = pd.DataFrame(list(results.items()), columns=['Reform', 'Net Income'])
    df['Difference'] = df['Net Income'] - df.loc[df['Reform'] == 'Baseline', 'Net Income'].values[0]
    df['Percent Change'] = (df['Difference'] / df.loc[df['Reform'] == 'Baseline', 'Net Income'].values[0]) * 100
    
    st.markdown("## Results")

    # Plotting
    df_plot = df[df["Reform"] != "Baseline"]  # Exclude baseline from plot
    fig = go.Figure()

    for _, row in df_plot.iterrows():
        fig.add_trace(go.Bar(
            x=[REFORMS[row["Reform"]]['name'] if row["Reform"] in REFORMS else row["Reform"]],
            y=[row["Difference"]],
            name=REFORMS[row["Reform"]]['name'] if row["Reform"] in REFORMS else row["Reform"],
            marker_color=REFORMS[row["Reform"]]['color'] if row["Reform"] in REFORMS else 'gray'
        ))

    fig.update_layout(
        title=f"Net Income Difference Comparison ({YEAR})",
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
    df_display["Reform"] = df_display["Reform"].map(lambda x: REFORMS[x]['name'] if x in REFORMS else x)
    df_display["Net Income"] = df_display["Net Income"].apply(lambda x: f"${x:,.2f}")
    df_display["Difference"] = df_display["Difference"].apply(lambda x: f"${x:,.2f}")
    df_display["Percent Change"] = df_display["Percent Change"].apply(lambda x: f"{x:.2f}%")

    st.write("Results Table:")
    st.dataframe(df_display.set_index("Reform"))

st.markdown(NOTES)
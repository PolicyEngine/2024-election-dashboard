import streamlit as st
import pandas as pd
import plotly.express as px


def render_reform_map():
    """Renders a map visualization of reform impacts by state."""

    # Load data from session state
    if "data" not in st.session_state:
        st.session_state.data = pd.read_csv("data/reform_impacts_2025.csv")
    data = st.session_state.data

    # Get selected reform and metric
    selected_reform = st.session_state.get(
        "selected_reform", data["reform_type"].iloc[0]
    )
    METRICS = {
        "Budgetary Impact ($B)": "cost",
        "Poverty Reduction (%)": "poverty_pct_cut",
        "Child Poverty Reduction (%)": "child_poverty_pct_cut",
        "Poverty Gap Reduction (%)": "poverty_gap_pct_cut",
        "Gini Index Reduction (%)": "gini_index_pct_cut",
    }
    selected_metric_name = st.selectbox("Select Metric", list(METRICS.keys()))
    metric_column = METRICS[selected_metric_name]

    # Filter data for selected reform
    reform_data = data[data["reform_type"] == selected_reform].copy()

    # Convert cost to billions
    reform_data["cost"] = reform_data["cost"] / 1e9

    # Create hover text with all metrics
    reform_data["hover_text"] = (
        "<b>"
        + reform_data["state"]
        + "</b><br>"
        + "Budgetary Impact: $"
        + reform_data["cost"].round(1).astype(str)
        + "B<br>"
        + "Poverty Reduction(%): "
        + reform_data["poverty_pct_cut"].round(1).astype(str)
        + "%<br>"
        + "Child Poverty Reduction (%): "
        + reform_data["child_poverty_pct_cut"].round(1).astype(str)
        + "%<br>"
        + "Poverty Gap Reduction (%): "
        + reform_data["poverty_gap_pct_cut"].round(1).astype(str)
        + "%<br>"
        + "Gini Index Reduction (%): "
        + reform_data["gini_index_pct_cut"].round(1).astype(str)
    )

    # Create choropleth map
    fig = px.choropleth(
        reform_data,
        locations="state",
        locationmode="USA-states",
        color=metric_column,
        scope="usa",
        color_continuous_scale=px.colors.diverging.RdBu,
        color_continuous_midpoint=0,
        title=f"{selected_metric_name} of the {selected_reform} by State",
        labels={metric_column: selected_metric_name},
        custom_data=["hover_text"],
    )

    # Update layout with centered title
    fig.update_layout(
        width=900,
        height=600,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},  # Increased top margin for title
        hoverlabel={"bgcolor": "white", "font_size": 14, "font_color": "black"},
        title={
            "text": f"{selected_metric_name} of the {selected_reform} by State",
            "y": 0.95,  # Adjust this value to move title up/down
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 20},  # Optional: adjust title font size
        },
    )

    # Update traces to use custom hover template
    fig.update_traces(
        hovertemplate="%{customdata[0]}<extra></extra>",
    )

    # Render with container width
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": True, "scrollZoom": True},
    )

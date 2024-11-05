import streamlit as st
import pandas as pd
import plotly.express as px


def get_metric_range(data, metric_column):
    """Get the maximum value for a given metric across all reforms"""
    return data[metric_column].max()


def render_reform_map():
    """Renders a map visualization of reform impacts by state."""

    # Load data from session state
    if "data" not in st.session_state:
        st.session_state.data = pd.read_csv("data/reform_impacts_2025.csv")
    data = st.session_state.data

    # Get selected values from session state
    selected_reform = st.session_state.selected_reform
    selected_metric_name = st.session_state.selected_metric
    metric_column = st.session_state.selected_metric_column

    # Filter data for selected reform
    reform_data = data[data["reform_type"] == selected_reform].copy()

    # Get the maximum value for the selected metric across all reforms
    max_value = data[metric_column].max()

    # Create hover text with all metrics
    reform_data["hover_text"] = (
        "<b>"
        + reform_data["state"]
        + "</b><br>"
        + "Average Household Impact: $"
        + reform_data["cost"].round(1).astype(str)
        + "<br>"
        + "Poverty Reduction(%): "
        + reform_data["poverty_pct_cut"].round(1).astype(str)
        + "%<br>"
        + "Gini Index Reduction (%): "
        + reform_data["gini_index_pct_cut"].round(1).astype(str)
    )

    # Create choropleth map with fixed range starting at 0
    fig = px.choropleth(
        reform_data,
        locations="state",
        locationmode="USA-states",
        color=metric_column,
        scope="usa",
        color_continuous_scale="Blues",
        range_color=[0, max_value],
        title=f"{selected_metric_name} of the {selected_reform} by State",
        labels={metric_column: selected_metric_name},
        custom_data=["hover_text"],
    )

    # Update layout with centered title
    fig.update_layout(
        width=900,
        height=600,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        hoverlabel={"bgcolor": "white", "font_size": 14, "font_color": "black"},
        title={
            "text": f"{selected_metric_name} of the {selected_reform} by State",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 20},
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

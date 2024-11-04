import streamlit as st
import pandas as pd
import plotly.express as px

def render_reform_map():
    """Renders a map visualization of reform impacts by state."""
    
    # Load data from session state
    if 'data' not in st.session_state:
        st.session_state.data = pd.read_csv("data/reform_impacts_2025.csv")
    data = st.session_state.data
    
    # Get selected reform and metric
    selected_reform = st.session_state.get('selected_reform', data['reform_type'].iloc[0])
    METRICS = {
        "Net Income Change (%)": "cost",
        "Poverty Rate Change (pp)": "poverty_pct_cut",  # Match to csv
        "Child Poverty Rate Change (pp)": "child_poverty_pct_cut",
        "Poverty Gap Change (%)": "poverty_gap_pct_cut",
        "Gini Change": "gini_index_pct_cut"
    }
    selected_metric_name = st.selectbox("Select Metric", list(METRICS.keys()))
    metric_column = METRICS[selected_metric_name]
    
    # Filter data for selected reform
    reform_data = data[data['reform_type'] == selected_reform][['state', metric_column]]
    reform_data = reform_data.rename(columns={metric_column: 'value'})  # Rename for Plotly compatibility
    
    # Create choropleth map
    fig = px.choropleth(
        reform_data,
        locations='state',
        locationmode="USA-states",
        color='value',
        scope="usa",
        color_continuous_scale=px.colors.diverging.RdBu,
        color_continuous_midpoint=0,
        title=f"Impact of {selected_reform} on {selected_metric_name} by State",
        labels={'value': selected_metric_name},
        hover_data={
            'state': True,
            'value': ':.2f'
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Display ranked table with unique states
    st.subheader("State Rankings")
    display_df = reform_data.sort_values('value', ascending=False).reset_index(drop=True)
    display_df['rank'] = display_df.index + 1
    display_df.columns = ['State', 'Impact', 'Rank']
    st.dataframe(display_df.round(2), hide_index=True, use_container_width=True)

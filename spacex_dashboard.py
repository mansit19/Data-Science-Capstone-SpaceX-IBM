import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# App layout
st.set_page_config(page_title="SpaceX Launch Dashboard", layout="wide")
st.title("🚀 SpaceX Launch Records Dashboard")

# Dropdown for launch site
launch_sites = ['All Sites'] + spacex_df['Launch Site'].unique().tolist()
selected_site = st.selectbox("Select a Launch Site", launch_sites)

# Pie Chart
st.subheader("🚀 Launch Success Pie Chart")
if selected_site == 'All Sites':
    filtered_df = spacex_df[spacex_df['class'] == 1]
    fig_pie = px.pie(filtered_df, names='Launch Site', title='Total Successful Launches by Site')
else:
    filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
    if filtered_df.empty:
        st.warning(f"No data available for site: {selected_site}")
        fig_pie = px.pie(names=['No Data'], values=[1], title=f'No launch data for {selected_site}')
    else:
        counts = filtered_df['class'].value_counts().reset_index()
        counts.columns = ['Launch Outcome', 'Count']
        counts['Launch Outcome'] = counts['Launch Outcome'].replace({1: 'Success', 0: 'Failure'})
        fig_pie = px.pie(counts, values='Count', names='Launch Outcome',
                         title=f'Success vs Failure for {selected_site}')
st.plotly_chart(fig_pie, use_container_width=True)

# Payload slider
st.subheader("📦 Payload Range (Kg)")
payload_range = st.slider("Select Payload Range (Kg)",
                          min_value=0, max_value=10000,
                          value=(min_payload, max_payload), step=1000)

# Scatter Plot
st.subheader("📈 Payload vs Launch Outcome Scatter Plot")
low, high = payload_range
filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]

if selected_site != 'All Sites':
    filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

fig_scatter = px.scatter(filtered_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title=f'Payload vs Outcome for {selected_site}',
                         labels={'class': 'Launch Outcome'},
                         hover_data=['Launch Site'])

st.plotly_chart(fig_scatter, use_container_width=True)

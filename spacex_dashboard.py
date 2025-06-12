import pandas as pd
import streamlit as st
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("spacex_launch_dash.csv")
    return df

spacex_df = load_data()

# Get payload limits
min_payload = int(spacex_df['Payload Mass (kg)'].min())
max_payload = int(spacex_df['Payload Mass (kg)'].max())

# App Title
st.title("🚀 SpaceX Launch Records Dashboard")
st.markdown("### Interactive Visualization of Launch Outcomes")

# Dropdown for Launch Site
site = st.selectbox(
    "Select Launch Site",
    options=['ALL'] + sorted(spacex_df['Launch Site'].unique().tolist()),
    index=0
)

# Pie Chart Section
st.subheader("Launch Success Pie Chart")

if site == 'ALL':
    filtered_df = spacex_df[spacex_df['class'] == 1]
    pie_fig = px.pie(filtered_df, names='Launch Site',
                     title='Total Successful Launches by Site')
else:
    filtered_df = spacex_df[spacex_df['Launch Site'] == site]
    if not filtered_df.empty:
        counts = filtered_df['class'].value_counts().reset_index()
        counts.columns = ['Launch Outcome', 'Count']
        counts['Launch Outcome'] = counts['Launch Outcome'].replace({1: 'Success', 0: 'Failure'})
        pie_fig = px.pie(counts, values='Count', names='Launch Outcome',
                         title=f'Success vs Failure for {site}')
    else:
        pie_fig = px.pie(names=['No Data'], values=[1], title='No launch data')

st.plotly_chart(pie_fig)

# Payload Slider
st.subheader("Payload Range (Kg)")
payload_range = st.slider(
    "Select Payload Range (Kg)",
    min_value=0,
    max_value=10000,
    value=(min_payload, max_payload),
    step=1000
)

# Scatter Plot Section
st.subheader("Payload vs Launch Outcome Scatter Chart")

# Filter data based on payload and site
low, high = payload_range
filtered_data = spacex_df[
    (spacex_df['Payload Mass (kg)'] >= low) &
    (spacex_df['Payload Mass (kg)'] <= high)
]

if site != 'ALL':
    filtered_data = filtered_data[filtered_data['Launch Site'] == site]

scatter_fig = px.scatter(
    filtered_data,
    x='Payload Mass (kg)',
    y='class',
    color='Booster Version Category',
    title=f"Payload vs Outcome for {'All Sites' if site == 'ALL' else site}",
    labels={'class': 'Launch Outcome'},
    hover_data=['Launch Site']
)

st.plotly_chart(scatter_fig)

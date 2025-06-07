# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    
    # Dropdown for launch site selection
    dcc.Dropdown(id='site-dropdown',  
             options=[
                {'label': 'All Sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
             ],
             value='ALL',
             placeholder="Select a Launch Site",
             searchable=True)
,
    html.Br(),

    # Pie chart for launch success
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),dcc.RangeSlider(
    id='payload-slider',
    min=0,
    max=10000,
    step=1000,
    marks={
        0: '0',
        1000: '1000',
        2000: '2000',
        3000: '3000',
        4000: '4000',
        5000: '5000',
        6000: '6000',
        7000: '7000',
        8000: '8000',
        9000: '9000',
        10000: '10000'
    },
    value=[min_payload, max_payload]
),

    # Scatter plot for payload vs success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(
            filtered_df,
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

        if filtered_df.empty:
            # Return an empty figure or a message
            fig = px.pie(
                names=['No Data'],
                values=[1],
                title=f'No launch data for site {entered_site}'
            )
            return fig

        counts = filtered_df['class'].value_counts().reset_index()
        counts.columns = ['Launch Outcome', 'Count']
        counts['Launch Outcome'] = counts['Launch Outcome'].replace({1: 'Success', 0: 'Failure'})

        fig = px.pie(
            counts,
            values='Count',
            names='Launch Outcome',
            title=f'Success vs Failure for site {entered_site}'
        )
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range  # unpack the payload slider range

    # Filter dataframe by payload range first
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]

    if selected_site == 'ALL':
        # Plot for all sites
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Outcome for All Sites',
            labels={'class': 'Launch Outcome'},
            hover_data=['Launch Site']
        )
    else:
        # Filter for the selected launch site
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Outcome for Site {selected_site}',
            labels={'class': 'Launch Outcome'},
            hover_data=['Launch Site']
        )

    return fig


# Run the app
if __name__ == '__main__':
    app.run()

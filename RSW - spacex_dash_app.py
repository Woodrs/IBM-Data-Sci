import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px

# Read the data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
assert 'Payload Mass (kg)' in spacex_df.columns, "DataFrame missing 'Payload Mass (kg)'"
assert 'class' in spacex_df.columns, "DataFrame missing 'class'"
assert 'Launch Site' in spacex_df.columns, "DataFrame missing 'Launch Site'"

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(id='site-dropdown',
                 options=[{'label': 'All Sites', 'value': 'ALL'},
                          {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                          {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                          {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}],
                 value='ALL', placeholder="Select a Launch Site here", searchable=True),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[min_payload, max_payload]),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output('success-pie-chart', 'figure'), Input('site-dropdown', 'value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df = filtered_df.groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        fig = px.pie(filtered_df, values='class count', 
        names='class', 
        title=f'Total Success Launches for {entered_site}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'), Input('payload-slider', 'value')])
def update_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_range[0], payload_range[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
        color='Booster Version Category', 
        title='Correlation between Payload and Success for All Sites')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
        color='Booster Version Category', 
        title=f'Correlation between Payload and Success for {entered_site}')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()

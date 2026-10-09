# Run: pip install pandas dash plotly ; python spacex_dash_app.py
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
spacex_df = pd.read_csv(URL)
max_payload, min_payload = spacex_df['Payload Mass (kg)'].max(), spacex_df['Payload Mass (kg)'].min()
sites = sorted(spacex_df['Launch Site'].unique())

app = Dash(__name__)
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center'}),
    dcc.Dropdown(id='site-dropdown',
                 options=[{'label': 'All Sites', 'value': 'ALL'}] + [{'label': s, 'value': s} for s in sites],
                 value='ALL', placeholder='Select a Launch Site', searchable=True),
    dcc.Graph(id='success-pie-chart'),
    html.P('Payload range (kg):'),
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                    marks={i: str(i) for i in range(0, 10001, 2500)}, value=[min_payload, max_payload]),
    dcc.Graph(id='success-payload-scatter-chart'),
])

@app.callback(Output('success-pie-chart', 'figure'), Input('site-dropdown', 'value'))
def pie(site):
    if site == 'ALL':
        return px.pie(spacex_df, values='class', names='Launch Site', title='Total successful launches by site')
    d = spacex_df[spacex_df['Launch Site'] == site]['class'].value_counts().reset_index()
    d.columns = ['class', 'count']
    return px.pie(d, values='count', names='class', title=f'Success vs failure at {site}')

@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'), Input('payload-slider', 'value')])
def scatter(site, payload):
    d = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0], payload[1])]
    if site != 'ALL':
        d = d[d['Launch Site'] == site]
    return px.scatter(d, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                      title='Payload vs launch outcome')

if __name__ == '__main__':
    app.run(debug=True)

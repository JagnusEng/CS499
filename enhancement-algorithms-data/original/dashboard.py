import dash
from dash import dcc, html, dash_table
import pandas as pd
from dash.dependencies import Input, Output

# ✅ USE SAMPLE DATA INSTEAD OF CONNECTING TO MONGODB
df = pd.DataFrame([
    {"animal_id": "A123", "name": "Max", "breed": "Labrador", "age": 3, "animal_type": "Dog", "location_lat": 30.2672, "location_long": -97.7431},
    {"animal_id": "B456", "name": "Bella", "breed": "Poodle", "age": 5, "animal_type": "Dog", "location_lat": 30.2672, "location_long": -97.7431},
    {"animal_id": "C789", "name": "Whiskers", "breed": "Siamese", "age": 2, "animal_type": "Cat", "location_lat": 30.2672, "location_long": -97.7431}
])

# Clean the data
df = df.fillna('')

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Grazioso Salvare Dashboard"),

    # Dropdown for filtering
    dcc.Dropdown(
        id='filter-dropdown',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'Dog', 'value': 'Dog'},
            {'label': 'Cat', 'value': 'Cat'},
            {'label': 'Reset', 'value': 'Reset'}
        ],
        value='All',
        placeholder="Filter by Animal Type"
    ),

    # Data Table
    dash_table.DataTable(
        id='data-table',
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict('records'),
        page_size=10
    ),

    # Bar Chart
    dcc.Graph(id='animal-type-chart'),

    # Geolocation Map
    dcc.Graph(id='geo-map')
])

# Update table based on dropdown filter
@app.callback(
    Output('data-table', 'data'),
    [Input('filter-dropdown', 'value')]
)
def update_table(selected_filter):
    if selected_filter == 'Reset' or selected_filter == 'All':
        return df.to_dict('records')
    else:
        filtered_df = df[df['animal_type'] == selected_filter]
        return filtered_df.to_dict('records')

# Update bar chart based on filter
@app.callback(
    Output('animal-type-chart', 'figure'),
    [Input('filter-dropdown', 'value')]
)
def update_chart(selected_filter):
    if selected_filter == 'Reset' or selected_filter == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['animal_type'] == selected_filter]

    if filtered_df.empty:
        return {
            'data': [],
            'layout': {
                'title': 'No Data Available',
                'xaxis': {'title': 'Animal Type'},
                'yaxis': {'title': 'Count'}
            }
        }

    animal_counts = filtered_df['animal_type'].value_counts()
    return {
        'data': [{'x': animal_counts.index, 'y': animal_counts.values, 'type': 'bar'}],
        'layout': {
            'title': 'Animal Type Distribution',
            'xaxis': {'title': 'Animal Type'},
            'yaxis': {'title': 'Count'}
        }
    }

# Update geolocation map based on filter
@app.callback(
    Output('geo-map', 'figure'),
    [Input('filter-dropdown', 'value')]
)
def update_map(selected_filter):
    if selected_filter == 'Reset' or selected_filter == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['animal_type'] == selected_filter]

    if filtered_df.empty:
        return {
            'data': [],
            'layout': {
                'title': 'No Data Available',
                'mapbox': {
                    'style': 'open-street-map',
                    'zoom': 5,
                    'center': {'lat': 30.2672, 'lon': -97.7431}
                }
            }
        }

    return {
        'data': [{
            'type': 'scattermapbox',
            'lat': filtered_df['location_lat'],
            'lon': filtered_df['location_long'],
            'mode': 'markers',
            'marker': {'size': 10},
            'text': filtered_df['animal_type']
        }],
        'layout': {
            'title': 'Rescue Locations',
            'mapbox': {
                'style': 'open-street-map',
                'zoom': 5,
                'center': {'lat': 30.2672, 'lon': -97.7431}
            }
        }
    }

# Run the app
if __name__ == '__main__':
    app.run(debug=True)


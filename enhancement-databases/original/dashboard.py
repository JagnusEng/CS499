import dash
from dash import dcc, html, dash_table
from pymongo import MongoClient
import pandas as pd
from dash.dependencies import Input, Output

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['animal_shelter']
collection = db['aac_outcomes']

# Load data from MongoDB
data = list(collection.find())

# Convert to DataFrame
df = pd.DataFrame(data)

# Reduce the dataset size for testing
df = df.head(100)

# Clean the data
df = df.drop(columns=['_id'], errors='ignore')  # Remove '_id' column if it exists
df = df.fillna('')  # Replace NaN values with empty strings

# Debugging: Print DataFrame information
print(f"Cleaned DataFrame shape: {df.shape}")
print(f"Cleaned DataFrame columns: {df.columns}")
print(df.head())

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    # Add the logo
    html.Img(
        src='/assets/Grazioso Salvare Logo.png',  # The path to the logo file
        style={'height': '100px', 'margin-bottom': '20px'}  # Adjust size and spacing
    ),

    html.H1("Grazioso Salvare Dashboard"),
    
    # Dropdown for filtering
    dcc.Dropdown(
        id='filter-dropdown',
       options=[
           {'label': 'All', 'value': 'All'},
           {'label': 'Dog', 'value': 'Dog'},
            {'label': 'Cat', 'value': 'Cat'},
           {'label': 'Reset', 'value': 'Reset'}  # Add Reset option
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
    dcc.Graph(
        id='animal-type-chart'
    ),

    # Geolocation Map
    dcc.Graph(
        id='geo-map'
    )
])

# Callback to update the DataTable based on filter
@app.callback(
    Output('data-table', 'data'),
    [Input('filter-dropdown', 'value')]
)
def update_table(selected_filter):
    try:
        # Handle Reset option
        if selected_filter == 'Reset':
            selected_filter = 'All'

        # Debugging: Print the selected filter
        print(f"Selected filter for table: {selected_filter}")

        # Filter the DataFrame based on the selected dropdown value
        if selected_filter == 'All':
            filtered_df = df
        else:
            filtered_df = df[df['animal_type'] == selected_filter]
        
        # Debugging: Print the filtered DataFrame shape
        print(f"Filtered DataFrame shape for table: {filtered_df.shape}")
        return filtered_df.to_dict('records')
    except Exception as e:
        print(f"Error in update_table callback: {e}")
        return []

# Callback to update the bar chart based on filter
@app.callback(
    Output('animal-type-chart', 'figure'),
    [Input('filter-dropdown', 'value')]
)
def update_chart(selected_filter):
    try:
        # Handle Reset option
        if selected_filter == 'Reset':
            selected_filter = 'All'

        # Debugging: Print the selected filter
        print(f"Selected filter for chart: {selected_filter}")

        # Filter the DataFrame based on the selected dropdown value
        if selected_filter == 'All':
            filtered_df = df
        else:
            filtered_df = df[df['animal_type'] == selected_filter]
        
        # Debugging: Print the filtered DataFrame shape
        print(f"Filtered DataFrame shape for chart: {filtered_df.shape}")

        if filtered_df.empty:
            # Return an empty chart if no data matches the filter
            return {
                'data': [],
                'layout': {
                    'title': 'No Data Available',
                    'xaxis': {'title': 'Animal Type'},
                    'yaxis': {'title': 'Count'}
                }
            }
        else:
            # Generate the bar chart
            animal_counts = filtered_df['animal_type'].value_counts()
            return {
                'data': [
                    {'x': animal_counts.index, 'y': animal_counts.values, 'type': 'bar'}
                ],
                'layout': {
                    'title': 'Animal Type Distribution',
                    'xaxis': {'title': 'Animal Type'},
                    'yaxis': {'title': 'Count'}
                }
            }
    except Exception as e:
        print(f"Error in update_chart callback: {e}")
        return {
            'data': [],
            'layout': {
                'title': 'Error Loading Chart',
                'xaxis': {'title': 'Animal Type'},
                'yaxis': {'title': 'Count'}
            }
        }

# Callback to update the geolocation map based on filter
@app.callback(
    Output('geo-map', 'figure'),
    [Input('filter-dropdown', 'value')]
)
def update_map(selected_filter):
    try:
        # Handle Reset option
        if selected_filter == 'Reset':
            selected_filter = 'All'

        # Debugging: Print the selected filter
        print(f"Selected filter for map: {selected_filter}")

        # Filter the DataFrame based on the selected dropdown value
        if selected_filter == 'All':
            filtered_df = df
        else:
            filtered_df = df[df['animal_type'] == selected_filter]
        
        # Debugging: Print the filtered DataFrame shape
        print(f"Filtered DataFrame shape for map: {filtered_df.shape}")

        if filtered_df.empty:
            # Return an empty map if no data matches the filter
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
        else:
            # Create the scatter mapbox chart
            return {
                'data': [
                    {
                        'type': 'scattermapbox',
                        'lat': filtered_df['location_lat'],
                        'lon': filtered_df['location_long'],
                        'mode': 'markers',
                        'marker': {'size': 10},
                        'text': filtered_df['animal_type']
                    }
                ],
                'layout': {
                    'title': 'Rescue Locations',
                    'mapbox': {
                        'style': 'open-street-map',
                        'zoom': 5,
                        'center': {'lat': 30.2672, 'lon': -97.7431}
                    }
                }
            }
    except Exception as e:
        print(f"Error in update_map callback: {e}")
        return {
            'data': [],
            'layout': {
                'title': 'Error Loading Map',
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


import dash
from dash import dcc, html, Input, Output, State
from dash import dash_table
import pandas as pd
from crud_module import create_animal, read_animals, update_animal, delete_animal

# Dash app initialization
app = dash.Dash(__name__)
server = app.server

# Helper to convert MongoDB data to DataFrame
def load_data():
    data = read_animals()
    for doc in data:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    return pd.DataFrame(data)

# Layout
app.layout = html.Div([
    html.H1("Grazioso Salvare Dashboard"),
    
    html.Div([
        dcc.Input(id='input_name', placeholder='Enter Name', type='text'),
        dcc.Input(id='input_breed', placeholder='Enter Breed', type='text'),
        dcc.Input(id='input_age', placeholder='Enter Age', type='number'),
        html.Button('Add Animal', id='btn_add'),
    ], style={'marginBottom': '20px'}),
    
    html.Div(id='add_message', style={'color': 'green'}),

    html.Div([
        dcc.Input(id='update_id', placeholder='Enter ID to update', type='text'),
        dcc.Input(id='update_age', placeholder='New Age', type='number'),
        html.Button('Update Age', id='btn_update')
    ], style={'marginBottom': '20px'}),
    
    html.Div(id='update_message', style={'color': 'blue'}),

    html.Div([
        dcc.Input(id='delete_id', placeholder='Enter ID to delete', type='text'),
        html.Button('Delete Animal', id='btn_delete')
    ], style={'marginBottom': '20px'}),
    
    html.Div(id='delete_message', style={'color': 'red'}),

    html.Hr(),

    html.H3("Animal Data"),
    dash_table.DataTable(
        id='animal_table',
        page_size=10,
        data=load_data().to_dict('records'),
        columns=[{'name': i, 'id': i} for i in load_data().columns]
    ),

    # Auto-refresh table every 3 seconds
    dcc.Interval(id='refresh', interval=3000, n_intervals=0)
])

# Add Animal
@app.callback(
    Output('add_message', 'children'),
    Input('btn_add', 'n_clicks'),
    State('input_name', 'value'),
    State('input_breed', 'value'),
    State('input_age', 'value'),
    prevent_initial_call=True
)
def add_animal(n_clicks, name, breed, age):
    if name and breed and age is not None:
        try:
            animal = {
                "name": name,
                "breed": breed,
                "age": int(age)
            }
            create_animal(animal)
            return "Animal added!"
        except Exception as e:
            return f"Error: {e}"
    return "Please fill all fields."

# Update Age
@app.callback(
    Output('update_message', 'children'),
    Input('btn_update', 'n_clicks'),
    State('update_id', 'value'),
    State('update_age', 'value'),
    prevent_initial_call=True
)
def update_animal_age(n_clicks, animal_id, age):
    if animal_id and age is not None:
        updated = update_animal(animal_id, {"age": int(age)})
        msg = "Updated successfully." if updated else "Update failed."
        return msg
    return "Provide valid ID and age."

# Delete Animal
@app.callback(
    Output('delete_message', 'children'),
    Input('btn_delete', 'n_clicks'),
    State('delete_id', 'value'),
    prevent_initial_call=True
)
def remove_animal(n_clicks, animal_id):
    if animal_id:
        deleted = delete_animal(animal_id)
        msg = "Deleted successfully." if deleted else "Delete failed."
        return msg
    return "Provide a valid ID."


# Refresh Table
@app.callback(
    Output('animal_table', 'data'),
    Input('refresh', 'n_intervals')
)
def refresh_table(n):
    return load_data().to_dict('records')

if __name__ == '__main__':
    app.run(debug=True)

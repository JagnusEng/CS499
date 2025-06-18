import dash
from dash import dcc, html, dash_table
import pandas as pd
from dash.dependencies import Input, Output, State

# ✅ SAMPLE DATA (replaces MongoDB connection)
df = pd.DataFrame([
    {"animal_id": "A123", "name": "Max"},
    {"animal_id": "B456", "name": "Bella"},
    {"animal_id": "C789", "name": "Whiskers"}
])

# Clean data
df = df.fillna('')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Img(src='/assets/Grazioso Salvare Logo.png'),
    html.H1("Grazioso Salvare Enhanced Dashboard"),

    html.Div([
        html.Label("Animal ID"),
        dcc.Input(id='animal_id', type='text'),

        html.Label("Name"),
        dcc.Input(id='animal_name', type='text'),

        html.Button('Add Animal', id='add_button', n_clicks=0),
        html.Button('Update Animal', id='update_button', n_clicks=0),
        html.Button('Delete Animal', id='delete_button', n_clicks=0),
    ], style={'padding': '10px', 'margin-bottom': '20px'}),

    dash_table.DataTable(
        id='animal_table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto'}
    ),

    html.Div(id='action_result')
])

# Store a copy of data globally for in-memory CRUD
data_store = df.copy()

@app.callback(
    Output('animal_table', 'data'),
    Input('add_button', 'n_clicks'),
    Input('update_button', 'n_clicks'),
    Input('delete_button', 'n_clicks'),
    State('animal_id', 'value'),
    State('animal_name', 'value')
)
def handle_crud(add, update, delete, animal_id, animal_name):
    global data_store
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if not animal_id:
        return data_store.to_dict('records')  # Skip action if ID is missing

    if "add_button" in changed_id:
        if animal_id not in data_store['animal_id'].values:
            data_store = pd.concat([data_store, pd.DataFrame([{"animal_id": animal_id, "name": animal_name}])])

    elif "update_button" in changed_id:
        mask = data_store['animal_id'] == animal_id
        if mask.any():
            data_store.loc[mask, 'name'] = animal_name

    elif "delete_button" in changed_id:
        data_store = data_store[data_store['animal_id'] != animal_id]

    return data_store.to_dict('records')

if __name__ == '__main__':
    app.run(debug=True)

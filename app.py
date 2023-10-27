from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
    html.H1('My Dash App'),  # Title

    dcc.Input(  # Text box
        id='my-textbox',
        type='number',
        placeholder='How many stocks you want?'
    ),

    dcc.Dropdown(  # Dropdown
        id='my-dropdown',
        options=[
            {'label': 'Option 1', 'value': 'OPT1'},
            {'label': 'Option 2', 'value': 'OPT2'}
        ],
        value='OPT1'
    ),

    dcc.Graph(  # Graph 1
        id='graph1',
        figure=fig1
    ),

    dcc.Graph(  # Graph 2
        id='graph2',
        figure=fig2
    ),

    dcc.Graph(  # Graph 3
        id='graph3',
        figure=fig3
    ),

    dcc.Graph(  # Graph 4
        id='graph4',
        figure=fig4
    ),

    html.Div(id='my-output')  # Text for displaying
])

if __name__ == '__main__':
    app.run_server(debug=True)

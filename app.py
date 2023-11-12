from dash import Dash, html, dcc, Input, Output, callback
from StockClasses import *
from pytickersymbols import PyTickerSymbols

stock_data = PyTickerSymbols()
all_tickers = {stock['symbol'] for stock in stock_data.get_all_stocks()}
all_tickers.remove(None)


default_stock = PracticeStockEvaluation("MSFT", 5, 1, 5)
fig1, fig2, fig3 = default_stock.get_fig()
market_cap = default_stock.get_market_cap()
earnings = default_stock.get_gains()

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('My Dash App'),  # Title

    html.Label('How many stocks you want?'),  # Label for input
    dcc.Input(  # Text box
        id='my-textbox',
        type='number',
        value=5
    ),

    html.Label('Select a ticker of wanted stock:'),  # Label for dropdown
    dcc.Dropdown(  # Dropdown
        id='my-dropdown',
        options=[
            {'label': ticker, 'value': ticker} for ticker in all_tickers
        ],
        value='MSFT'
    ),

    html.Label('Training data the model know exist'),  # Label for graph 1
    dcc.Graph(  # Graph 1
        id='graph1',
        figure=fig1
    ),

    html.Label('Evaluating data the model does not know exist'),  # Label for graph 2
    dcc.Graph(  # Graph 2
        id='graph2',
        figure=fig2
    ),

    html.Label('Showing how well the model can track local minimums and maximums for deciding when to buy and sell '
               'stocks'),  # Label for graph 3
    dcc.Graph(
        id='graph3',
        figure=fig3
    ),

    html.Div(id='my-output', children=f'Market Cap: {market_cap}\nEarnings: {earnings}')  # Text for displaying
])


@callback([Output(component_id='graph1', component_property='figure'),
           Output(component_id='graph2', component_property='figure'),
           Output(component_id='graph3', component_property='figure'),
           Output(component_id='my-output', component_property='children')],
          [Input(component_id='my-dropdown', component_property='value'),
           Input(component_id='my-textbox', component_property='value')])
def update_graphs(stock_ticker, stock_amount):
    current_stock = PracticeStockEvaluation(stock_ticker, stock_amount, 1, 5)
    figure_1, figure_2, figure_3 = current_stock.get_fig()
    current_market_cap = current_stock.get_market_cap()
    current_earnings = current_stock.get_gains()
    return figure_1, figure_2, figure_3, f'Market Cap: {current_market_cap}\nEarnings: {current_earnings}'


if __name__ == '__main__':
    app.run_server(debug=True)

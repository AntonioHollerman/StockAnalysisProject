from dash import Dash, html, dcc, Input, Output, callback
from StockClasses import *

STARTING_STOCKS = 5
TRAINING_MONTHS = 1
EVAL_MONTHS = 5

all_tickers = {'GD', 'OMC', 'MKC', 'FIS', 'LOGN', 'APH', 'ETSY', 'CVX', 'ZBH', 'EVRG', 'EVT', 'IPG', 'UDR', 'VLO', 'JD', 'POOL', 'STZ', 'NDAQ', 'HYDR', 'III', 'ARGX', 'EZM', 'IBM', 'DAL', 'HLN', 'SBS', 'ALC', 'DPZ', 'XYL', 'RBSFY', 'APD', 'HPE', 'BKT', 'BME', 'MET', 'BDX', 'L', 'TDG', 'CB', 'NEE', 'LRCX', 'ALV', 'JKHY', 'CE', 'TRMB', 'FOXA', 'MGM', 'ASSA B', 'CPB', 'WM', 'CLX', 'MELI', 'BKNG', 'CAG', 'XEL', 'GLPG', 'DHR', 'CF', 'CVS', 'AEP', 'HIG', 'GILD', 'ITP', 'SNPS', 'PM', 'CDW', 'CPT', 'FDS', 'REE', 'AZO', 'PARA', 'HES', 'QRVO', 'HSY', 'TXN', 'WAT', 'DTE', 'ATVI', 'HSIC', 'DOCU', 'WRB', 'LOW', 'A', 'WDAY', 'BSL', 'HM B', 'ARE', 'AMD', 'MAS', 'SHB A', 'MCO', 'GLW', 'RHM', 'HRL', 'GL', 'STT', 'BMY', 'WRK', 'COF', 'BN', 'HAL', 'INTC', 'AMS', 'VIV', 'BR', 'DVA', 'ANSS', 'CFR', 'MAA', 'TXT', 'PGR', 'LUV', 'ETR', 'PTC', 'MCK', 'ULTA', 'PWR', 'SVT', 'CPRT', 'SCHW', 'FFIV', 'HLT', 'BXP', 'EQR', 'PSX', 'KEY', 'WY', 'GRF', 'TSLA', 'INCY', 'CRL', 'IEX', 'WEC', 'NEM', 'TGT', 'CNA', 'SRE', 'CI', 'BLND', 'PNC', 'FIVE', 'WYNN', 'DTG', 'MSCI', 'EIX', 'BB', 'PCAR', 'AIZ', 'TTWO', 'EW', 'DOV', 'CSX', 'SEDG', 'TDY', 'ESS', 'VALN', 'CCI', 'SBUX', 'JNJ', 'DXC', 'TSCO', 'NDA DK', 'DHI', 'TEL2 B', 'DLTR', 'AMCR', 'ZION', 'IVZ', 'SPLK', 'DUK', 'EBAY', 'NOC', 'CAH', 'FRES', 'CINF', 'GWW', 'SNA', 'LMT', 'NOW', 'RTO', 'ILMN', 'NKE', 'EMN', 'OKE', 'APTV', 'NPACY', 'WBA', 'BRK-B', 'CL', 'HPQ', 'ELUX B', 'DDOG', 'ATCO A', 'HBAN', 'MC', 'ANET', 'MRK', 'KMX', 'MOR', 'RL', 'MKTX', 'INTU', 'CGUSY', 'ISP', 'ROG', 'AAPL', 'BEN', 'MMC', 'ZS', 'BBY', 'TJX', 'DE', 'HAS', 'TFX', 'AZN', 'REGN', 'ROP', 'CCL', 'CTEC', 'KMB', 'AKAM', 'UAL', 'HII', 'AMT', 'EUTLF', 'FE', 'BBVA', 'TRV', 'LLY', 'EQIX', 'MGNT', 'META', 'ICE', 'EDV', 'MDT', 'AME', 'MTB', 'GRMN', 'ADM', 'AWK', 'BK', 'AMAT', 'ABBV', 'BAX', 'VZ', 'BA', 'PEAK', 'NWL', 'IP', 'NTRS', 'CWC', 'WFC', 'CTSH', 'PYPL', 'TPR', 'EXC', 'AOS', 'GEN', 'MSI', 'LVS', 'HOLX', 'TCS', 'CTVA', 'TEL', 'DVN', 'MRO', 'VICI', 'WDC', 'MPWR', 'SKF B', 'ROK', 'EL', 'GNRC', 'AOF', 'NVR', 'FDX', 'AHT', 'VRSK', 'PSN', 'WMB', 'AON', 'FMC', 'CRM', 'FCX', 'GBF', 'QCOM', 'CTLT', 'ERMAY', 'MMM', 'PKG', 'CARM', 'BBWI', 'UNH', 'ACGL', 'TMO', 'FTV', 'MTX', 'AI', 'LAND', 'JPM', 'NXT', 'CME', 'BIDU', 'IFF', 'TSN', 'MOH', 'DFS', 'RCL', 'SCA A', 'NCLH', 'AMP', 'ESSITY B', 'COO', 'KR', 'CMA', 'ALK', 'SKANSKA B', 'STM', 'CPG', 'URI', 'ALRS', 'KIM', 'KEYS', 'ISRG', 'AFL', 'FTNT', 'ALLE', 'VTS', 'LYV', 'ABNB', 'PG', 'CHTR', 'CBOE', 'KDP', 'CTAS', 'VTRS', 'RF', 'SANDVIK A', 'AGOAF', 'TER', 'GS', 'NFLX', 'JNPR', 'LH', 'DGX', 'TAP', 'XRAY', 'WELL', 'CGGYY', 'KHC', 'MEIYF', 'TECH', 'CBRE', 'SGE', 'DOW', 'NWSA', 'SYY', 'EXR', 'SO', 'PEG', 'AAL', 'MSFT', 'C', 'ADTN', 'K', 'RMD', 'MRNA', 'AEE', 'NDSN', 'HEXA B', 'WBD', 'REG', 'SAN', 'V', 'FITB', 'PSA', 'YUM', 'LCID', 'BIIB', 'INVH', 'ROL', 'D', 'AVB', 'AIG', 'ECL', 'OTIS', 'CMCSA', 'RHI', 'MT', 'CHRW', 'JCI', 'CSCO', 'ZM', 'AES', 'BOSS', 'SHW', 'ORA', 'ORLY', 'PSH', 'SYK', 'MBG', 'WAB', 'SAP', 'STX', 'PAYX', 'ALGN', 'RIO', 'HON', 'CNP', 'CMI', 'IR', 'EMR', 'AXP', 'DRI', 'ML', 'GSK', 'KMI', 'ITW', 'TROW', 'RSG', 'CRH', 'BSX', 'RJF', 'HCA', 'ON', 'COP', 'UTG', 'KO', 'DSM', 'OXY', 'VFC', 'MOS', 'CNC', 'SECU B', 'GRUPF', 'NN', 'SGEN', 'IQV', 'MTD', 'SU', 'BAC', 'TEAM', 'EFX', 'GIS', 'JBHT', 'CMG', 'KINV B', 'PAYC', 'CZR', 'GPN', 'PPG', 'OKTA', 'TRGP', 'SSAB A', 'AJG', 'TMUS', 'MAR', 'PRU', 'NVDA', 'VRBCF', 'IHG', 'O', 'AIR', 'FRT', 'HD', 'AGS', 'VOD', 'UPS', 'ALB', 'ED', 'APAM', 'SIRI', 'ENR', 'SEE', 'BWA', 'BF-B', 'BOIVF', 'EOG', 'CAT', 'LIN', 'CDNS', 'LNC', 'ORCL', 'ZTS', 'GM', 'ZBRA', 'MTCH', 'T', 'FRA', 'SLB', 'HUM', 'PXD', 'MRVL', 'BRO', 'FANG', 'OR', 'DISH', 'CSGP', 'NRG', 'BKR', 'TEF', 'LYB', 'ASM', 'ABT', 'EXPD', 'MNST', 'VNO', 'UNP', 'BIO', 'DXCM', 'SWKS', 'EA', 'HWM', 'WNDLF', 'VMC', 'ENG', 'F', 'GOOGL', 'SPGI', 'ES', 'AVGO', 'MO', 'ADSK', 'RAND', 'ADI', 'APA', 'LW', 'MA', 'ADP', 'USB', 'GE', 'AMZN', 'GSEFF', 'RS', 'MLM', 'SLOIF', 'ENPH', 'PCG', 'LEG', 'KLAC', 'FLT', 'SBNY', 'DG', 'DIS', 'TYL', 'NSC', 'PANW', 'WMT', 'NTES', 'HEI', 'VTR', 'NXPI', 'PPL', 'HST', 'GPC', 'IDXX', 'PLD', 'STLA', 'PEP', 'MHK', 'JCDXF', 'MCD', 'MPC', 'BNR', 'PFG', 'LKQ', 'CFG', 'AMGN', 'DLR', 'LULU', 'CHD', 'ELV', 'PNR', 'LHX', 'ALL', 'OZON', 'AAP', 'ASML', 'OGN', 'SMIN', 'MCHP', 'NTAP', 'PNW', 'BLK', 'FTK', 'SJM', 'LEN', 'ATO', 'MDLZ', 'IRM', 'FAST', 'NXPRF', 'WST', 'CRWD', 'ADBE', 'ROST', 'TFC', 'IAG', 'IT', 'SYF', 'ODFL', 'VBVBF', 'LUMN', 'ACN', 'SPG', 'ACA', 'UHS', 'PDD', 'PHM', 'SWED A', 'WPP', 'TT', 'EQT', 'WHR', 'SBAC', 'MU', 'XOM', 'NI', 'SWK', 'CTRA', 'GETI B', 'CDAY', 'PH', 'CARR', 'EXPE', 'ETN', 'IDR', 'NUE', 'LNT', 'VRTX', 'EPAM', 'MS', 'COST', 'LDOS', 'VRSN', 'AVY', 'CMS'}


default_stock = PracticeStockEvaluation("MSFT", STARTING_STOCKS, TRAINING_MONTHS, EVAL_MONTHS)
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

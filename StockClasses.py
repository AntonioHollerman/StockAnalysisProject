from ModelingStocks import *
import pytz
from dateutil.relativedelta import relativedelta
import plotly.express as px
import plotly.graph_objects as go


class Portfolio:
    def __init__(self):
        pass

    def get_market_cap(self):
        pass

    def get_gains(self):
        pass


class Stock:
    def __init__(self, ticker: str):
        pass

    def update_value(self):
        pass

    def find_next_zero(self):
        pass

    def get_fig(self):
        pass

    def buy(self):
        pass

    def sell(self):
        pass


class PracticeStockEvaluation:
    def __init__(self, ticker: str, amount_of_stocks: int, months_of_train: int, months_of_evaluating: int,
                 tz: str = "America/New_York"):
        self.stocks_owned = 0
        self.capital = 0
        self.price = 0
        self.starting_cap = 0
        self.tz = pytz.timezone(tz)

        start_train = self.tz.localize(dt.now()) - relativedelta(months=months_of_train + months_of_evaluating)
        end_train = self.tz.localize(dt.now()) - relativedelta(months=months_of_evaluating)
        start_eval = end_train
        end_eval = self.tz.localize(dt.now())

        self.stock_df, self.scaler, self.x_origin = format_data(ticker, (start_train, end_eval))
        self.model = create_model(self.stock_df, (start_train, end_train))
        self.stock_df['yhat'] = self.model.predict(self.stock_df[['Scaled']].to_numpy())

        self.train_df: pd.DataFrame = self.stock_df[(self.stock_df['Date'] >= start_train) & (self.stock_df['Date'] <= end_train)]
        self.eval_df: pd.DataFrame = self.stock_df[(self.stock_df['Date'] >= start_eval) & (self.stock_df['Date'] <= end_eval)]

        self.zeros = get_zeros(self.func_derv,
                               self.sec_derv,
                               [self.eval_df[['X']].min(), self.eval_df[['X']].max()],
                               'neg')
        self.zeros.sort()
        first_zero, is_max = self.zeros[0]

        if is_max:
            self.set_time(0)
            self.stocks_owned = amount_of_stocks
            self.starting_cap = amount_of_stocks * self.price
            self.set_time(first_zero)
            self.sell()
        else:
            self.set_time(first_zero)
            self.stocks_owned = amount_of_stocks
            self.starting_cap = amount_of_stocks * self.price

        for zero, is_max in self.zeros[1:]:
            self.set_time(zero)
            if is_max:
                self.sell()
            else:
                self.buy()

    def get_market_cap(self):
        return self.stocks_owned * self.price + self.capital

    def get_gains(self):
        return self.get_market_cap() - self.starting_cap

    def set_time(self, x):
        date = self.tz.localize(dt.fromtimestamp(x + self.x_origin))
        holding_df: pd.DataFrame = self.stock_df[self.stock_df['Date'] <= date]
        self.price = holding_df.loc[holding_df['Date'] == holding_df[['Date']].max(), 'Close'].item()

    def get_fig(self):
        data = self.train_df.copy()
        data.sort_values(by='Date', inplace=True)
        fig1 = px.line(data, x='Date', y='Close')
        fig2 = px.line(data, x='Date', y='yhat')
        fig2.update_traces(line_color='red')
        figure_1 = go.Figure(data=fig1.data + fig2.data)
        figure_1.update_xaxes(title_text='Date')
        figure_1.update_yaxes(title_text='Stock Price')

        test_data = self.eval_df.copy()
        test_data.sort_values(by='Date', inplace=True)
        fig1 = px.line(test_data, x='Date', y='Close')
        fig2 = px.line(test_data, x='Date', y='yhat')
        fig2.update_traces(line_color='red')
        figure_2 = go.Figure(data=fig1.data + fig2.data)
        figure_2.update_xaxes(title_text='Date')
        figure_2.update_yaxes(title_text='Stock Price')

        holding_dict = {'Date': [], 'yhat': []}
        for x, _ in self.zeros:
            holding_dict['Date'].append(self.tz.localize(dt.fromtimestamp(x + self.x_origin)))
            holding_dict['yhat'].append(self.func(x))
        zeros_df = pd.DataFrame(holding_dict)
        zeros_df.sort_values(by='Date', inplace=True)
        fig1 = px.line(zeros_df, x='Date', y='yhat')
        fig2 = px.line(test_data, x='Date', y='yhat')
        fig2.update_traces(line_color='red')
        figure_3 = go.Figure(data=fig1.data + fig2.data)
        figure_3.update_xaxes(title_text='Date')
        figure_3.update_yaxes(title_text='Stock Price')
        
        return figure_1, figure_2, figure_3

    def buy(self):
        self.stocks_owned = self.capital // self.price
        self.capital = self.capital - self.stocks_owned * self.price

    def sell(self):
        self.capital = self.capital + self.stocks_owned * self.price
        self.stocks_owned = 0

    def func(self, x):
        value_ = pd.DataFrame({'X': [x]})
        return self.model.predict(self.scaler.transform(value_))[0]

    def func_derv(self, x):
        return derivative(self.func, x)

    def sec_derv(self, x):
        return derivative(self.func_derv, x)

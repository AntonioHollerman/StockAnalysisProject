from typing import Tuple
from datetime import datetime as dt
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures, StandardScaler, FunctionTransformer
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from scipy.optimize import root_scalar
import concurrent.futures


class AsymptoteSpottedError(Exception):
    def __init__(self, message="Asymptote spotted"):
        self.message = message
        super().__init__(self.message)


def format_data(ticker: str, data_range: Tuple[dt, dt], train_range: Tuple[dt, dt]):
    data: pd.DataFrame = yf.download(ticker, start=data_range[0], end=data_range[1])
    data = data[['Close']].reset_index()
    x_origin = data['Date'].min().timestamp()
    data['X'] = data['Date'].apply(lambda x: x.timestamp() - x_origin)
    train_data: pd.DataFrame = data[(data['Date'] >= train_range[0]) & (data['Date'] <= train_range[1])].copy()
    scaler = StandardScaler().fit(train_data[['X']])
    data['Scaled'] = scaler.transform(data[['X']])
    return data.copy(), scaler, x_origin


def create_model(df, train_range: Tuple[dt, dt]):
    start, end = train_range
    data: pd.DataFrame = df[(df['Date'] >= start) & (df['Date'] <= end)].copy()
    x = data[['Scaled']].to_numpy()
    y = data[['Close']].to_numpy()

    pipe = make_pipeline(FunctionTransformer(), PolynomialFeatures(), Ridge())
    param_grid = {'polynomialfeatures__degree': [16],
                  'ridge__alpha': [0.01, 0.1, 1.0],
                  'ridge__copy_X': [True, False],
                  'ridge__solver': ['lsqr'],
                  'ridge__tol': [0.001, 0.01, 0.1],
                  'functiontransformer__func': [np.sin, np.cos],  # Functions to try
                  'functiontransformer__inverse_func': [np.arcsin, np.arccos],  # Inverse functions to try
                  'functiontransformer__validate': [True, False],  # Whether to validate the input
                  'functiontransformer__accept_sparse': [True, False],  # Whether to accept sparse matrix inputs
                  'functiontransformer__check_inverse': [False],  # Whether to check the inverse function
                  }
    grid = GridSearchCV(pipe, param_grid, cv=5, scoring='r2')
    grid.fit(x, y)
    return grid.best_estimator_


def derivative(f, x):
    delta_x = 10
    numerator = f(x + delta_x) - f(x)
    denom = (delta_x + x) - x
    return numerator / denom


def find_zero(f, x0, x1):
    if f(x0)*f(x1) < 0:  # If the function crosses zero between x0 and x1
        root = root_scalar(f, method='brentq', bracket=[x0, x1])
        return root.root


def get_zeros(f, f_prime, range_, sign_wanted):
    # Define the range
    min_, max_ = range_
    x_range = np.linspace(min_, max_, int((max_ - min_) // 86400))

    # Find zeros in the range
    zeros = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(find_zero, f, x_range[i], x_range[i+1]) for i in range(len(x_range)-1)]
        for future in concurrent.futures.as_completed(futures):
            root = future.result()
            if root is not None:
                zeros.append(root)

    cond_list = []
    # Calculate the value of the derivative at x
    for zero in zeros:
        derivative_value = f_prime(zero)

        # If derivative zero then it is an Asymptote
        if derivative_value == 0:
            raise AsymptoteSpottedError

        # Check the direction of the zero crossing
        if sign_wanted == "pos":
            cond_list.append(derivative_value > 0)
        else:
            cond_list.append(derivative_value < 0)
    return [(zero, cond[0]) for zero, cond in (zip(zeros, cond_list))]

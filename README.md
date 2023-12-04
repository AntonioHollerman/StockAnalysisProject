# Python Stock Bot
___
## Summary
This project creates a regression model in python predict local minimums and local 
maximums of a stock market cap. At local minimus the bot will preform a "Buy" and 
local maximums will perform a "Sell". Model is developed from sci-kit learn regression 
model and local minimus/maximus are found using calculus.

## Evaluation App
To evaluate the performance of both my regression model and buying/selling logic I created 
a dash app to display visuals of the stocks training market cap, predicted market cap, 
where buys/sells are happening, and the gains/loss if the model was used 3 months ago. 
Created "Dummy Classes" that are only used for this app to preform fake buys and fake sells.

##### Dashboard Link: [App](https://stock-analysis-project-699427999309.herokuapp.com/)

## How Model Created
I decided to have one month of stock data for training and 5 months of unseen stock data to evaluate on.
For example April - May for training and May - October for evaluating. Took
this approach to simulate the model will not have access to future stock trends 
but will make an attempt to predict them. 

###### Code is not use in production but is an example.
``` python
import yfinance as yf
tz = pytz.timezone("America/New_York")
start = tz.localize(dt(2023, 4, 27))
end = tz.localize(dt(2023, 5, 27))

ticker = "MSFT"
train_data = yf.download(ticker, start=start, end=end)

start = tz.localize(dt(2023, 5, 27))
end = tz.localize(dt(2023, 10, 27))

ticker = "MSFT"
test_data = yf.download(ticker, start=start, end=end)
```
Now that I have my training and evaluating data sets I will format the 
data in a way easy to handle. Instead of feeding the model dates that are
used for the column provided by yfinance I converted the dates into seconds 
using timestamp() method and subtracted by the smallest time step to represent the 
origins. 

###### Function used to pre-process my data
```py
def format_data(ticker: str, data_range: Tuple[dt, dt], train_range: Tuple[dt, dt]):
  data: pd.DataFrame = yf.download(ticker, start=data_range[0], end=data_range[1])
  data = data[['Close']].reset_index()
  x_origin = data['Date'].min().timestamp()
  data['X'] = data['Date'].apply(lambda x: x.timestamp() - x_origin)
  train_data: pd.DataFrame = data[(data['Date'] >= train_range[0]) & (data['Date'] <= train_range[1])].copy()
  scaler = StandardScaler().fit(train_data[['X']])
  data['Scaled'] = scaler.transform(data[['X']])
  return data.copy(), scaler, x_origin
```
Finally, I dumped the training data into a regression model with modified parameters. The most important
aspect is that repeating functions are included (ex: sine and cosine) because if the model values are not repeating
outside the training range will drop or rise an alarming rate without turning.
###### Function used to create my model
```python
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
```
## How Local Mins and Local Maxs Located
A property that a function have is that at an x value if its derivative is zero then that point is a min or max.
By using my model as a function, to find local mins/maxs all I need to do is find the zeros of its derivative. 
Right after creating the model for the stock at hand I create a method in the same class for its derivative.
I also need the second derivative to determine if the x-value a max or min. If the second derivative
at x is positive then it is a min else then it is a max.

###### This is the function for getting the "slope" at a point
```python
def derivative(f, x):
    delta_x = 10
    numerator = f(x + delta_x) - f(x)
    denom = (delta_x + x) - x
    return numerator / denom
```
###### These are the two methods that wrapped the function above
```python
def func_derv(self, x):
    return derivative(self.func, x)

def sec_derv(self, x):
    return derivative(self.func_derv, x)
```
## Future Versions of Project
The end result of this project is to have a website that allows the user to easily
invest money in stocks and allow my stock bot preforms buys and sells on the investment
to maximize the users profit.
#### Version 1.0 (Current Version)
* Create function to pre-process data input/output
* Create function the develops regression model
* Create function to find local mins/maxs
* Create methods to buy and sell
* Create logic on when to buy and sell
#### Version 1.5
* Change model from training on one big data set to more iteratively as new data get introduced
* Update buy/sell logic
  * Not to buy when last time sold stocks is less than current market cap
  * Not to sell when last time bought stocks is greater than current market cap
#### Version 2
* Drag over logic from dummy classes to the production classes
* Create Buy and Sell methods for the production classes
  * Use an API to deal with real stocks
#### Version 3 
* Create a PostgreSQL database to hold users information
  * Market cap
  * login
  * models
  * etc.
* Create website for users to use our stocks
  * (Can not go into the details of development process
because I do not have experience making web apps)
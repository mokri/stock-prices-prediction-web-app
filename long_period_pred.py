# ## Importing all the necessary Libraries

# Necessary libraries = Pandas, fbprophet and plotly

# pandas= data Manipulation and analysis
# fbprophet = Forecasting
# plotly= data visualization

import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go


def prepare_dataset(df):
    date = pd.DataFrame(df.index)
    date = date['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    date = date.to_list()
    close = df['Close'].to_list()
    prophet_df = pd.DataFrame({'ds': date, 'y': close})

    return prophet_df


# Creating Facebook Prophet Model
def predict(prophet_df, period):
    prophet_df = prophet_df.loc[prophet_df['ds'] > '2019']

    model = Prophet()
    model.fit(prophet_df)

    # Forecasting
    # predict X days in the future
    future = model.make_future_dataframe(periods=period, include_history=False)
    forecast = model.predict(future)
    forecast = forecast.rename(columns={'ds': 'Date', 'yhat': 'Close', 'yhat_upper': 'High', 'yhat_lower': 'Low'})
    forecast = forecast[['Date', 'Close', 'High', 'Low']]
    return forecast


def charts(predictions):
    open = predictions[['Close']][:-1]
    predictions = predictions[1:]
    predictions.insert(1, 'Open', open['Close'].to_list())
    # fig = px.box(predictions, x='Date', y=['Close', 'High', 'Low'])

    fig = go.Figure(data=[go.Candlestick(x=predictions['Date'],
                                         open=predictions['Open'],
                                         high=predictions['High'],
                                         low=predictions['Low'],
                                         close=predictions['Close']
                                         )])

    # fig.update_layout(width=900, height=600)
    return fig


def next_x_days_pred(df, num_days):
    prepared_df = prepare_dataset(df)
    predictions = predict(prepared_df, num_days)
    predictions_chart = charts(predictions)
    return predictions[3:], predictions_chart

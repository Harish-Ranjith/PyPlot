# Modules
from datetime import datetime, timedelta
import pandas as pd
import pandas_datareader as pdr
import plotly.graph_objects as go
import csv

import yfinance as yf
from datetime import datetime, timedelta
CRYPTO = input("Enter the symbol of the cryptocurrency: ")
CURRENCY = input("Enter the currency: ")
SYMBOL = input("Enter the symbol of your currency: ")
TIMELINE = int(input("Enter the number of days: "))


# Fetch data
# def getData(cryptocurrency):
#     now = datetime.now()
#     current_date = now.strftime("%Y-%m-%d")
#     last_year_date = (now - timedelta(days=TIMELINE)).strftime("%Y-%m-%d")

#     start = pd.to_datetime(last_year_date)
#     end = pd.to_datetime(current_date)

#     data = pdr.get_data_yahoo(f'{cryptocurrency}-{CURRENCY}', start, end)

#     return data

CRYPTO = 'BTC'
CURRENCY = 'USD'
SYMBOL = '$'
TIMELINE = 30  # Try a larger window

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
last_date = (now - timedelta(days=TIMELINE)).strftime("%Y-%m-%d")

data = yf.download(f'{CRYPTO}-{CURRENCY}', start=last_date, end=current_date)

# Flatten columns if MultiIndex
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

print(data[['Open', 'High', 'Low', 'Close']].tail())

# Check for empty data
if data[['Open', 'High', 'Low', 'Close']].isnull().all().all():
    print("No valid data available for the selected period.")
else:
    # Plot as before
    import plotly.graph_objects as go
    fig = go.Figure(data=[
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        )
    ])
    fig.show()



def getData(cryptocurrency):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    last_year_date = (now - timedelta(days=TIMELINE)).strftime("%Y-%m-%d")

    data = yf.download(f'{cryptocurrency}-{CURRENCY}', start=last_year_date, end=current_date)
    return data



crypto_data = getData(CRYPTO)
print(list(crypto_data))
# Candlestick
fig = go.Figure(
    data=[
        go.Candlestick(
            x=crypto_data.index,
            open=crypto_data.Open,
            high=crypto_data.High,
            low=crypto_data.Low,
            close=crypto_data.Close
        ),
        go.Scatter(
            x=crypto_data.index,
            y=crypto_data.Close.rolling(window=20).mean(),
            mode='lines',
            name='20SMA',
            line={'color': '#ff006a'}
        ),
        go.Scatter(
            x=crypto_data.index,
            y=crypto_data.Close.rolling(window=50).mean(),
            mode='lines',
            name='50SMA',
            line={'color': '#1900ff'}
        )
    ]
)

fig.update_layout(
    title=f'The Candlestick graph for {CRYPTO}',
    xaxis_title='Timeline',
    yaxis_title=f'Price ({CURRENCY})',
    xaxis_rangeslider_visible=False
)
fig.update_yaxes(tickprefix=SYMBOL)

fig.show()


def createCSVFile():
    filename = input("Enter the name of the file with .csv extension: ")
    with open(filename, "w") as fh:
        writeit = csv.writer(fh)
        writeit.writerow(list(crypto_data))


createCSVFile()

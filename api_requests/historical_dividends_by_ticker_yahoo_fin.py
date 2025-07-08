import yfinance as yf
import pandas as pd

def get_historical_dividends_get(ticker='KO'):
    t = yf.Ticker(ticker)
    dividends = t.dividends
    if dividends is None or dividends.empty:
        return pd.DataFrame(columns=['date', 'dividend', 'ticker'])
    df = dividends.reset_index()
    df.columns = ['date', 'dividend']
    df['ticker'] = ticker
    return df

def get_historical_dividends(ticker='KO', time_delta=60):
    """
    Get historical dividends for a ticker using yfinance
    This is the function that app.py expects
    """
    return get_historical_dividends_get(ticker)

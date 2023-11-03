from yahoo_fin.stock_info import get_dividends


def get_historical_dividends_get(ticker='KO'):
    return get_dividends(ticker=ticker, index_as_date=False)

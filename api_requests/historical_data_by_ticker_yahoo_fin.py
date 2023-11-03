from yahoo_fin.stock_info import get_data


def get_historical_data_get(ticker='KO', start_date='2022-10-14', end_date='2023-10-24'):
    return get_data(ticker, start_date=start_date, end_date=end_date, index_as_date=False)

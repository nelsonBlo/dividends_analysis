from datetime import datetime
from api_requests.historical_data_by_ticker_yahoo_fin import get_historical_data_get
from misc.utils import get_latest_file
from misc.utils import save_response_to_csv
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('./conf/general.conf')
INITIAL_PART_HISTORICAL_DATA_TICKER = config.get('FILE_NAMES', 'INITIAL_PART_HISTORICAL_DATA_TICKER')


def get_historical_data(ticker='KO', start_date='', end_date='', days_delta=1):
    file_name = f'{INITIAL_PART_HISTORICAL_DATA_TICKER}{ticker}'
    latest_file = get_latest_file(file_name=file_name, days_delta=days_delta)

    if latest_file:
        try:
            return pd.read_csv(latest_file)
        except:
            raise SystemExit(
                f"\033[91m Can not open file {latest_file} or does not have proper format. \033[0m")
    else:
        final_part = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f'{INITIAL_PART_HISTORICAL_DATA_TICKER}{ticker}_{final_part}.csv'
        response_json = get_historical_data_get(ticker, start_date, end_date)
        save_response_to_csv(response_json, file_name, index=False)
    return response_json

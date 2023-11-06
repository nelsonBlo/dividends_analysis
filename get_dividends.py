from datetime import datetime
from misc.utils import tune_investing_response_and_save
from misc.utils import get_latest_file
from api_requests.dividends_by_date_investing import get_dividends_next_week_post
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('./conf/general.conf')
INITIAL_PART_DIVIDENDS_BY_DATE = config.get('FILE_NAMES', 'INITIAL_PART_DIVIDENDS_BY_DATE')


def get_dividends_next_week(country=5, filter_time='nextWeek'):
    file_name = f'{INITIAL_PART_DIVIDENDS_BY_DATE}{country}'
    latest_file = get_latest_file(file_name)
    if latest_file:
        try:
            with open(latest_file) as f:
                return pd.read_csv(latest_file)
        except:
            raise SystemExit(
                f"\033[91m Can not open file {latest_file} or does not have proper format. \033[0m")
    else:
        final_part = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f'{INITIAL_PART_DIVIDENDS_BY_DATE}{country}_{final_part}.csv'
        response_json = get_dividends_next_week_post(country=country, filter_time=filter_time)
        return tune_investing_response_and_save(response_json, file_name)

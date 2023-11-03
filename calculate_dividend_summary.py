from datetime import datetime
from misc.utils import get_latest_file
from misc.utils import save_response_to_csv
import pandas as pd
import get_dividends_historical_by_ticker
import configparser

config = configparser.ConfigParser()
config.read('./conf/general.conf')
INITIAL_PART_DIVIDENDS_SCORECARD = config.get('FILE_NAMES', 'INITIAL_PART_DIVIDENDS_SCORECARD')

# INITIAL_PART_DIVIDENDS_SCORECARD = 'dividends_scorecard_'


def get_dividend_summary(ticker="KO", time_delta=60):
    file_name = f'{INITIAL_PART_DIVIDENDS_SCORECARD}{ticker}'
    latest_file = get_latest_file(file_name=file_name, days_delta=time_delta)

    if latest_file:
        try:
            with open(latest_file) as f:
                return pd.read_csv(latest_file, index_col=None)
        except:
            raise SystemExit(
                f"\033[91m Can not open file {latest_file} or does not have proper format. \033[0m")
    else:
        final_part = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f'{INITIAL_PART_DIVIDENDS_SCORECARD}{ticker}_{final_part}.csv'
        df = get_dividends_historical_by_ticker.get_historical_dividends(ticker)
        df["date"] = pd.to_datetime(df["date"])
        df["mode"] = df["date"].dt.year.value_counts().mode()
        data = [[df.head(1)["date"][0].year, df.head(1)["dividend"][0],
                 "Quarterly" if df["mode"][0] == 4 else "Monthly" if df["mode"][0] == 12 else "Other"]]
        dg = pd.DataFrame(data, columns=['First Div. Paid (Year)', 'First Div. Paid (US$)', 'Div. Frequency'])
        save_response_to_csv(dg, file_name)
    return dg

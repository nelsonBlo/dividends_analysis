from datetime import datetime
from misc.utils import get_latest_file
from misc.utils import save_response_to_csv
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('./conf/general.conf')
INITIAL_PART_DIVIDENDS_SUMMARY = config.get('FILE_NAMES', 'INITIAL_PART_DIVIDENDS_SUMMARY')


def get_dividend_summary(data=None, time_delta=60):
    ticker = data[0]['ticker']
    file_name = f'{INITIAL_PART_DIVIDENDS_SUMMARY}{ticker}'
    latest_file = get_latest_file(file_name=file_name, days_delta=time_delta)

    if latest_file:
        try:
           return pd.read_csv(latest_file, index_col=None)
        except:
            raise SystemExit(
                f"\033[91m Can not open file {latest_file} or does not have proper format. \033[0m")
    else:
        final_part = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f'{INITIAL_PART_DIVIDENDS_SUMMARY}{ticker}_{final_part}.csv'
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df.sort_values(by='date', ascending=True, inplace=True)
        df["mode"] = int(df["date"].dt.year.value_counts().mode())
        df["mode"] = df["mode"].iloc[-1]
        df = df.head(1)
        data = [[df["date"].dt.year.iloc[0], df["dividend"].iloc[0],
                 "Quarterly" if df["mode"].iloc[0] == 4 else "Monthly" if df["mode"].iloc[0] == 12 else "Other"]]
        dg = pd.DataFrame(data, columns=['First Div. Paid (Year)', 'First Div. Paid (US$)', 'Div. Frequency'])
        save_response_to_csv(dg, file_name)
    return dg

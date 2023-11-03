import numpy as np
import os
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

days_list = ['Monday,', 'Tuesday,', 'Wednesday,', 'Thursday,', 'Friday,']
headers = ["Date", "Company (Ticker)", "Ex-Dividend Date", "Dividend", "Payment Date", "Yield"]


def tune_investing_response_and_save(response, filename):
    soup = BeautifulSoup(response["data"], 'html.parser')

    li_tags = soup.find_all('a')
    tickers = []
    for li in li_tags:
        tickers.append(li.get_text())
    cleantext = BeautifulSoup(response["data"], "lxml").text

    list_of_results = cleantext.splitlines()
    list_of_results[:] = [item for item in list_of_results if item]

    position_list = []
    for k, v in enumerate(list_of_results):
        if v.split(" ", 1)[0] in days_list:
            position_list.append((v, k))

    position_list_rev = []
    counter = int(len(list_of_results))
    for k, v in reversed(list(enumerate(list_of_results))):
        if v.split(" ", 1)[0] in days_list:
            position_list_rev.append((v, int((counter - 1 - k) / 5)))
            counter = k

    position_list_rev.reverse()
    clearl_list = [i for i in list_of_results if i.split(" ", 1)[0] not in days_list]
    contador = 0
    for k, v in enumerate(position_list_rev):
        for _ in range(0, v[1]):
            clearl_list.insert(contador, v[0])
            contador += 6

    list_as_df = pd.DataFrame(np.reshape(np.array(clearl_list), (int(len(clearl_list) / 6), 6)),
                              columns=headers)
    save_response_to_csv(list_as_df, filename)
    return list_as_df


def save_response_to_csv(list_as_df, filename, index=False):
    try:
        list_as_df.to_csv(f'./csv_files/{filename}', index = index)
    except:
        raise SystemExit(
            f"\033[91m Can not save file {filename} on local system. \033[0m")


def get_latest_file(file_name='', days_delta=1):
    latest_file = ''
    list_of_files = []
    for filename in os.listdir('./csv_files/'):
        if filename.startswith(f'{file_name}') and filename.endswith('csv'):
            list_of_files.append(f'./csv_files/{filename}')

    if list_of_files:
        latest_file = max(list_of_files, key=os.path.getctime)
        c_time = os.path.getctime(latest_file)
        if datetime.now() - datetime.fromtimestamp(c_time) >= timedelta(hours=days_delta):
            latest_file = None
    return latest_file

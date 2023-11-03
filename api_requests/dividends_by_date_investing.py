from curl_cffi import requests
import configparser

config = configparser.ConfigParser()
config.read('./conf/general.conf')
url = config.get('INVESTING', 'URL')
endpoint = config.get('INVESTING', 'ENDPOINT')


def get_dividends_next_week_post(country=5, filter_time='nextWeek'):
    headers = {
        "x-requested-with": "XMLHttpRequest",
    }
    body = {
        "country[]": country,
        "currentTab": filter_time,
        "limit_from": 0
    }
    api_result = requests.post(url=f'{url}{endpoint}',
                               data=body,
                               headers=headers,
                               impersonate="chrome101")
    return api_result.json()

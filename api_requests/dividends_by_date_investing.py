from curl_cffi import requests
import configparser
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    
    try:
        logger.info(f"Making request to: {url}{endpoint}")
        
        api_result = requests.post(url=f'{url}{endpoint}',
                                   data=body,
                                   headers=headers,
                                   impersonate="chrome101")
        
        logger.info(f"Response status: {api_result.status_code}")
        
        if api_result.status_code != 200:
            logger.error(f"API returned status code: {api_result.status_code}")
            return {"data": []}  # Return empty data to prevent crash
        
        try:
            return api_result.json()
        except Exception as e:
            logger.error(f"Failed to parse JSON: {e}")
            logger.error(f"Response text (first 500 chars): {api_result.text[:500]}")
            return {"data": []}  # Return empty data to prevent crash
            
    except Exception as e:
        logger.error(f"Request failed: {e}")
        return {"data": []}  # Return empty data to prevent crash

from requests import Request, Session  # Import necessary libraries
import json
import pprint
import csv
from config import *
from common.price_conversion import *

def read_csv(file_name='data.csv'):
    """
    Read data from a CSV file and return a list of dictionaries.

    Args:
        file_name (str): Name of the CSV file (default: 'data.csv')
    
    Returns:
        list: List of dictionaries representing the CSV data
        list: List of headers representing the CSV data
    """
    data_list = []
    headers = []

    with open(file_name, 'r') as file:
        csv_reader = csv.DictReader(file)
        headers = csv_reader.fieldnames

        for row in csv_reader:
            data_list.append(dict(row))
    return headers, data_list

def getCmkInfo(tickers):
    """
    Get cryptocurrency information from CoinMarketCap API.

    Args:
        tickers (list): List of ticker symbols

    Returns:
        dict: Dictionary containing cryptocurrency information
    """
    tickers_str = ",".join(tickers)

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = { 'symbol': tickers_str, 'convert': 'USD' }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_API_KEY

        #'X-CMC_PRO_API_KEY': '1d90b9e5-c373-41ba-8e3f-13627c7ca16f'
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    return  json.loads(response.text)

def parseCmkInfo(coins_info, data):
    """
    Extract relevant cryptocurrency information from CoinMarketCap API response.

    Args:
        coins_info (dict): Dictionary to store the extracted information
        data (dict): CoinMarketCap API response data

    Returns:
        dict: Updated dictionary containing cryptocurrency information
    """
    cmk_coins = data['data'].values()

    for cmk_coin in cmk_coins:
        coin = {
            CFG_STR_CMC_RANK: cmk_coin[CFG_STR_CMC_RANK],
            CFG_STR_CMC_DATE_ADDED: cmk_coin[CFG_STR_CMC_DATE_ADDED],
            CFG_STR_CMC_SYMBOL: cmk_coin[CFG_STR_CMC_SYMBOL],
            CFG_STR_CMC_NAME: cmk_coin[CFG_STR_CMC_NAME],
            #'tags': cmk_coin['tags'],
            CFG_STR_CMC_PRICE: cmk_coin['quote']['USD'][CFG_STR_CMC_PRICE],
            CFG_STR_CMC_CHANGE_1H: format_float(cmk_coin['quote']['USD'][CFG_STR_CMC_CHANGE_1H]),
            CFG_STR_CMC_CHANGE_24H: format_float(cmk_coin['quote']['USD'][CFG_STR_CMC_CHANGE_24H]),
            CFG_STR_CMC_CHANGE_7D: format_float(cmk_coin['quote']['USD'][CFG_STR_CMC_CHANGE_7D]),
            CFG_STR_CMC_CHANGE_30D: format_float(cmk_coin['quote']['USD'][CFG_STR_CMC_CHANGE_30D]),
            CFG_STR_CMC_CHANGE_60D: format_float(cmk_coin['quote']['USD'][CFG_STR_CMC_CHANGE_60D]),
            CFG_STR_CMC_CHANGE_90D: format_float(cmk_coin['quote']['USD'][CFG_STR_CMC_CHANGE_90D]),
        }
        coins_info[cmk_coin[CFG_STR_CMC_SYMBOL]] =  coin

    return coins_info

import pprint
import csv
import argparse
import os
import sys
from cmkp import *
from config import *

def convert_to_float(s):
    ret_val = s

    try:
        ret_val = float(s)
        return ret_val
    except:
        return ret_val

def addUserData(coins_info, user_coins, user_headers):
    for user_coin in user_coins:
        symbol = user_coin['Ticker']
        if symbol not in coins_info:
            print("Missing %s" % symbol)
            continue

        #print(user_coin)
        for head in user_headers:
            #print(head)
            coins_info[symbol][head] = user_coin[head]

            coins_info[symbol][head] = convert_to_float(user_coin[head])
def addUserData2(coins_info, user_coins):
    
    cmkp_headers = coins_info[list(coins_info.keys())[0]].keys()

    for user_coin in user_coins:
        symbol = user_coin['Ticker']
        print("|%s|" % {symbol})
        #print("|", symbol, "|start", coins_info[symbol])

        #pprint.pprint(coins_info.keys())
        if symbol not in coins_info.keys():
            print("Missing %s" % symbol)
            continue

        #print(user_coin)
        for head in cmkp_headers:
            #print(cmkp_headers)
            #coins_info[symbol][head] = user_coin[head]

            user_coin[head] = convert_to_float(coins_info[symbol][head])

def createELkBulkFile(coins_info):
    with open('output.json', 'w') as file:
        for key, value in coins_info.items():
            file.write(json.dumps({"index": {"_id": key}}) + '\n')
            file.write(json.dumps(value) + '\n')

def createUpdatedCsvFile(csv_file_path, data):
    # Extract the keys from the first inner dictionary to be used as header
    inner_fields = list(data.values())[0].keys()

    # Write the inner data to the CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=inner_fields)

        # Write the header
        csv_writer.writeheader()

        # Write the inner data
        for inner_dict in data.values():
            csv_writer.writerow(inner_dict)

    print(f"CSV file '{csv_file_path}' with inner dictionaries has been created.")

def createUpdatedCsvFile2(csv_file_path, data):
    # Extract the keys from the first inner dictionary to be used as header
    inner_fields = data[0].keys()
    print(inner_fields)
    #print("----------------------------------------------------------")
    #pprint.pprint(data)
    #print("============================")

    # Write the inner data to the CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=inner_fields)

        # Write the header
        csv_writer.writeheader()

        # Write the inner data
        for coin in data:
            print(">>>>>>>>>>>>>", coin)
            csv_writer.writerow(coin)

    print(f"CSV file '{csv_file_path}' with inner dictionaries has been created.")


def add_defaualt_values_for_new_fileds(coins_info):
    for key, value in coins_info.items():
                value[CFG_STR_BUY] = 0
                value[CFG_STR_BUY_MINIMAL_PERC_DROP] = 100
                value[CFG_STR_BUY_OPTIMAL_PERC_DROP] = 100
                value[CFG_STR_BUY_60X_PERC_DROP] = 100
                #value[CFG_STR_BUY_GENERATIONAL_PERC_DROP] = 100

def _should_buy(coins_info, buy_catagory, buy_catagory_percent_drop, buy_weight):
    for key, value in coins_info.items():
            if (value[buy_catagory] != 0):
                value[buy_catagory_percent_drop] = round(((value[CFG_STR_CMC_PRICE] - value[buy_catagory]) / value[CFG_STR_CMC_PRICE]) * 100, 2)

            if value[CFG_STR_CMC_PRICE] < value[buy_catagory]:
                value[CFG_STR_BUY] = buy_weight


def calculate_buy_in_info(coins_info):
    _should_buy(coins_info, CFG_STR_BUY_MINIMAL, CFG_STR_BUY_MINIMAL_PERC_DROP, 1)
    _should_buy(coins_info, CFG_STR_BUY_OPTIMAL, CFG_STR_BUY_OPTIMAL_PERC_DROP, 2)
    _should_buy(coins_info, CFG_STR_BUY_60X, CFG_STR_BUY_60X_PERC_DROP, 3)
    #_should_buy(coins_info, CFG_STR_BUY_GENERATIONAL, CFG_STR_BUY_GENERATIONAL_PERC_DROP, 4)


def update_watch_list_info(input_file, output_file):
    coins_info = {}

    user_headers, user_data = read_csv(input_file)


    # DBG
    #print(user_headers)
    #print(user_data)

    tickers = []

    for coin in user_data:
        tickers.append(coin['Ticker'])

    # Get cryptocurrency information from CoinMarketCap API
    data = getCmkInfo(tickers)

    # Extract relevant information and populate the coins_info dictionary
    parseCmkInfo(coins_info, data)

    addUserData(coins_info, user_data, user_headers)
    # Print the final coins_info dictionary
    #pprint.pprint(coins_info)

    add_defaualt_values_for_new_fileds(coins_info)
    calculate_buy_in_info(coins_info)
    # Create a new csv file will all the new data
    createUpdatedCsvFile(output_file, coins_info)

def update_protfolio_info(input_file, output_file):
    coins_info = {}

    user_headers, user_data = read_csv(input_file)


    # DBG
    #print(user_headers)
    #print(user_data)

    tickers = []

    for coin in user_data:
        tickers.append(coin['Ticker'])

    # Get cryptocurrency information from CoinMarketCap API
    data = getCmkInfo(tickers)

    # Extract relevant information and populate the coins_info dictionary
    parseCmkInfo(coins_info, data)

    addUserData2(coins_info, user_data)
    # Print the final coins_info dictionary
    pprint.pprint(len(user_data))
    pprint.pprint(user_data)

    # Create a new csv file will all the new data
    createUpdatedCsvFile2(output_file, user_data)

# Create an argument parser
parser = argparse.ArgumentParser()

parser.add_argument('--watch_list_file', default=CFG_FILE_WATCHLIST_INPUT, help='CSV file name')
parser.add_argument('--protfolio_file', default=CFG_FILE_PROTFOLIO_INPUT, help='CSV file name')

# Parse the command-line arguments
args = parser.parse_args()

if not os.path.exists(args.watch_list_file) and not os.path.exists(args.protfolio_file):
    sys.exit('You must provide at least one file (did not find any on the disk)')


# Read CSV based on the provided file name
if os.path.exists(args.watch_list_file):
    update_watch_list_info(args.watch_list_file, CFG_FILE_WATCHLIST_OUTPUT)

if os.path.exists(args.protfolio_file):
    update_protfolio_info(args.protfolio_file, CFG_FILE_PROTFOLIO_OUTPUT)

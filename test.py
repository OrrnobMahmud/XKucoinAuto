import time
import requests
import urllib.parse
import os
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def read_data_file(file_path):
    accounts = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            encoded_data = line.strip()
            if encoded_data:
                accounts.append(encoded_data)
    return accounts

def decode_data(encoded_data):
    params = dict(item.split('=') for item in encoded_data.split('&'))
    return {
        "decoded_user": urllib.parse.unquote(params['user']),
        "decoded_start_param": urllib.parse.unquote(params['start_param']),
        "hash": params['hash'],
        "auth_date": params['auth_date'],
        "chat_type": params['chat_type'],
        "chat_instance": params['chat_instance']
    }

def login(decoded_data):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/login?lang=en_US"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-request-with": "null",
        "Referer": "https://www.kucoin.com/miniapp/tap-game?inviterUserId=5496274031&rcode=QBSTAPN3"
    }
    body = {
        "inviterUserId": "5496274031",
        "extInfo": {
            "hash": decoded_data['hash'],
            "auth_date": decoded_data['auth_date'],
            "via": "miniApp",
            "user": decoded_data['decoded_user'],
            "chat_type": decoded_data['chat_type'],
            "chat_instance": decoded_data['chat_instance'],
            "start_param": decoded_data['decoded_start_param']
        }
    }
    session = requests.Session()
    response = session.post(url, headers=headers, json=body)
    cookie = '; '.join([f"{cookie.name}={cookie.value}" for cookie in session.cookies])             
    return cookie, session

def get_account_data(session, cookie):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/summary?lang=en_US"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-request-with": "null",
        "Referer": "https://www.kucoin.com/miniapp/tap-game?inviterUserId=5496274031&rcode=QBSTAPN3",
        "cookie": cookie
    }
    response = session.get(url, headers=headers)
    data = response.json()
    return data['data']

def tap(session, cookie, molecule, max_taps=3000):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/gold/increase?lang=en_US"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-request-with": "null",
        "Referer": "https://www.kucoin.com/miniapp/tap-game?inviterUserId=5496274031&rcode=QBSTAPN3",
        "cookie": cookie
    }
    form_data = {
        'increment': '1',
        'molecule': str(molecule)
    }
    taps_done = 0
    for _ in range(max_taps):
        response = session.post(url, headers=headers, data=form_data)
        data = response.json()
        if data.get('code') == '200000':  # Assuming this is the success code
            taps_done += 1
            if taps_done % 100 == 0:  # Log every 100 taps
                logging.info(f"Tapped {taps_done}/{max_taps}")
        else:
            logging.error(f"Tap failed: {data.get('msg', 'Unknown error')}")
            break
        time.sleep(0.5)  # 0.5 second delay between taps to avoid rate limiting
    return taps_done

def process_accounts():
    file_path = "data.txt"
    encoded_data_list = read_data_file(file_path)
    total_accounts = len(encoded_data_list)
    account_last_tap = {i: datetime.min for i in range(total_accounts)}
    
    while True:
        clear_terminal()
        logging.info(f"Total accounts: {total_accounts}")

        for index, encoded_data in enumerate(encoded_data_list):
            current_time = datetime.now()
            time_since_last_tap = current_time - account_last_tap[index]
            
            if time_since_last_tap.total_seconds() < 1500:
                remaining_cooldown = 1500 - time_since_last_tap.total_seconds()
                logging.info(f"Account {index + 1} is cooling down. {remaining_cooldown:.0f} seconds remaining.")
                continue
            
            logging.info(f"Processing account number - {index + 1}")
            decoded_data = decode_data(encoded_data)
            cookie, session = login(decoded_data)
            account_data = get_account_data(session, cookie)
            
            logging.info(f"Account {index + 1} data:")
            logging.info(f"Current Balance: {account_data['availableAmount']}")
            logging.info(f"Total Taps: {account_data['totalTapCount']}")
            logging.info(f"Daily Taps: {account_data['dailyTapCount']}")
            
            molecule = account_data['feedPreview']['molecule']
            taps_done = tap(session, cookie, molecule)
            
            new_account_data = get_account_data(session, cookie)
            logging.info(f"New Balance: {new_account_data['availableAmount']}")
            
            account_last_tap[index] = current_time
            
            if taps_done < 3000:
                logging.info(f"Tapping stopped at {taps_done}. Moving to next account.")
            else:
                logging.info(f"Completed 3000 taps for account {index + 1}.")
            
            time.sleep(2)  # Short delay between accounts
        
        logging.info("Completed a full cycle. Waiting for 60 seconds before next cycle...")
        time.sleep(60)  # Wait for 1 minute before starting the next cycle

if __name__ == "__main__":
    process_accounts()

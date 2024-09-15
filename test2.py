import time
import requests
import random
import urllib.parse
import os
from colorama import Fore, Style, init
from datetime import datetime, timedelta

# Initialize colorama for color output
init(autoreset=True)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Blum Auto style banner
def art(total_accounts, use_proxy):
    print(Fore.GREEN + Style.BRIGHT + r"""
    ┌────────────────────────────────────────────────────┐
    │ Orrnob Drops Automation Project                    │
    │        Auto Claim For XKucoinFrog                  │
    └────────────────────────────────────────────────────┘
    Author  : Orrnob Mahmud
    Github  : https://github.com/OrrnobMahmud
    """ + Style.RESET_ALL)
    
    print(Fore.GREEN + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] total account : {total_accounts}")
    print(Fore.GREEN + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] use proxy : {use_proxy}")
    print(Fore.GREEN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

# Function to read data from 'data.txt'
def read_data_file(file_path):
    accounts = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            encoded_data = line.strip()
            if encoded_data:
                accounts.append(encoded_data)
    return accounts

# Function to decode the account information
def decode_data(encoded_data):
    params = dict(item.split('=') for item in encoded_data.split('&'))

    decoded_user = urllib.parse.unquote(params['user'])
    decoded_start_param = urllib.parse.unquote(params['start_param'])

    return {
        "decoded_user": decoded_user,
        "decoded_start_param": decoded_start_param,
        "hash": params['hash'],
        "auth_date": params['auth_date'],
        "chat_type": params['chat_type'],
        "chat_instance": params['chat_instance']
    }

# Function to handle account login
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
    return cookie

# Function to retrieve account data
def data(cookie):
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
    
    response = requests.get(url, headers=headers)
    data = response.json()
    balance = data.get("data", {}).get("availableAmount")
    molecule = data.get("data", {}).get("feedPreview", {}).get("molecule")
    print(f"{Fore.GREEN}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Balance: {balance}")
    return molecule

# Updated function to tap/increment gold in account
def tap(cookie, molecule, max_taps=3000, retry_delay=5, max_retries=3):
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
    start_time = datetime.now()
    
    for _ in range(max_taps):
        retries = 0
        while retries < max_retries:
            response = requests.post(url, headers=headers, data=form_data)
            data = response.json()
            if data.get('success') == True:
                taps_done += 1
                if taps_done % 100 == 0:  # Log every 100 taps
                    current_time = datetime.now()
                    elapsed_time = (current_time - start_time).total_seconds()
                    print(f"{Fore.GREEN}[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Tapped {taps_done}/{max_taps} (Elapsed: {elapsed_time:.2f}s)")
                time.sleep(0.5)  # Reduced wait time between taps
                break
            elif data.get('code') == '4000010':  # 'less increase interval' error
                print(f"{Fore.YELLOW}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Rate limited. Waiting {retry_delay} seconds before retry.")
                time.sleep(retry_delay)
                retries += 1
            else:
                print(f"{Fore.RED}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Tap failed. Full response: {data}")
                return taps_done
        else:
            print(f"{Fore.RED}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Max retries reached. Moving to next account.")
            return taps_done
    
    return taps_done

# Function to check new balance after tapping
def new_balance(cookie):
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
    
    response = requests.get(url, headers=headers)
    data = response.json()
    balance = data.get("data", {}).get("availableAmount")
    print(f"{Fore.GREEN}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] New Balance: {balance}")

# Updated function to process accounts
def process_accounts():
    file_path = "data.txt"  # Your file containing accounts
    encoded_data_list = read_data_file(file_path)
    total_accounts = len(encoded_data_list)
    
    account_last_tap = {i: datetime.min for i in range(total_accounts)}
    
    while True:
        clear_terminal()  # Clear terminal before displaying banner
        art(total_accounts, use_proxy=False)  # Display banner
        
        for index, encoded_data in enumerate(encoded_data_list):
            current_time = datetime.now()
            time_since_last_tap = current_time - account_last_tap[index]
            
            if time_since_last_tap.total_seconds() < 3600:  # 1 hour cooldown
                remaining_cooldown = 3600 - time_since_last_tap.total_seconds()
                print(f"{Fore.YELLOW}[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Account {index + 1} cooling down. {remaining_cooldown:.0f}s remaining.")
                continue
            
            print(f"{Fore.GREEN}[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Processing account {index + 1}")
            decoded_data = decode_data(encoded_data)
            cookie = login(decoded_data)
            molecule = data(cookie)
            taps_done = tap(cookie, molecule)
            new_balance(cookie)
            
            account_last_tap[index] = current_time
            
            if taps_done < 3000:
                print(f"{Fore.YELLOW}[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Tapping stopped at {taps_done} for account {index + 1}.")
            else:
                print(f"{Fore.GREEN}[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Completed 3000 taps for account {index + 1}.")
            
            time.sleep(2)  # Short delay between accounts
        
        print(f"{Fore.GREEN}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Completed a full cycle. Waiting for 5 minutes before next cycle...")
        time.sleep(300)  # Wait for 5 minutes before starting the next cycle

if __name__ == "__main__":
    process_accounts()

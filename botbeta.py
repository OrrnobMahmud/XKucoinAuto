import time
import requests
import random
import urllib.parse
import os
from colorama import Fore, Style, init
from datetime import datetime

# Initialize colorama for color output
init(autoreset=True)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Blum Auto style banner
def art(total_accounts, use_proxy):
    print(Fore.MAGENTA + Style.BRIGHT + r"""
    ┌────────────────────────────────────────────────────┐
    │ Orrnob Drops Automation Project                    │
    │        Auto Claim For XKucoinFrog                         │
    └────────────────────────────────────────────────────┘
    Author  : Orrnob Mahmud
    Github  : https://github.com/OrrnobMahmud
    """ + Style.RESET_ALL)
    
    print(Fore.GREEN + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] total account : {total_accounts}")
    print(Fore.CYAN + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] use proxy : {use_proxy}")
    print(Fore.YELLOW + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

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
    balance = data.get("data").get("availableAmount")
    molecule = data.get("data").get("feedPreview").get("molecule")
    print(f"{Fore.GREEN + Style.BRIGHT}Balance: {Fore.WHITE + Style.BRIGHT}{balance}")
    return molecule

# Function to tap/increment gold in account
def tap(cookie, increment, molecule):
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
        'increment': str(increment),
        'molecule': str(molecule)
    }
    
    for _ in range(15):
        response = requests.post(url, headers=headers, data=form_data)
        data = response.json()
        colors = [Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
        random_color = random.choice(colors)
        print(f"{random_color}{Style.BRIGHT}Tapped{Style.RESET_ALL}")
        time.sleep(2)

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
    balance = data.get("data").get("availableAmount")
    print(f"{Fore.MAGENTA + Style.BRIGHT}New Balance: {balance}")

# Function to process accounts, including the logic for login, tap, and new balance
def process_accounts():
    file_path = "data.txt"  # Your file containing accounts
    encoded_data_list = read_data_file(file_path)
    total_accounts = len(encoded_data_list)
    
    while True:
        clear_terminal()  # Clear terminal before displaying banner
        art(total_accounts, use_proxy=False)  # Display Blum Auto banner

        # Process each account
        for index, encoded_data in enumerate(encoded_data_list, start=1):
            print(f"{Fore.GREEN}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] account number - {index}")
            decoded_data = decode_data(encoded_data)
            cookie = login(decoded_data)
            molecule = data(cookie)
            increment = random.randint(40, 60)
            tap(cookie, increment, molecule)
            new_balance(cookie)
            time.sleep(2)
        
        print(f"{Fore.YELLOW}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Waiting for 2 minutes before next cycle...")
        time.sleep(120)  # Wait for 2 minutes (120 seconds)

if __name__ == "__main__":
    process_accounts()


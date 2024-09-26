import time
import requests
import random
import urllib.parse
import os
import signal
from colorama import Fore, Style, init
from datetime import datetime
from fake_useragent import UserAgent  # Import fake-useragent library

# Initialize colorama for color output
init(autoreset=True)

# Global variable to control the main loop
running = True

def signal_handler(signum, frame):
    global running
    running = False
    print(Fore.LIGHTBLACK_EX + f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
          Fore.YELLOW + "Received interrupt signal. Preparing to exit...")

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def art(total_accounts):
    print(Fore.GREEN + Style.BRIGHT + r"""
   ___                   _      __  __      _                 _ 
  / _ \ _ _ _ _ _ _  ___| |__  |  \/  |__ _| |_  _ __ _  _ __| |
 | (_) | '_| '_| ' \/ _ \ '_ \ | |\/| / _` | ' \| '  \ || / _` |
  \___/|_| |_| |_||_\___/_.__/ |_|  |_\__,_|_||_|_|_|_\_,_\__,_| 
                                                                
    Auto Claim Bot For XkuCoin - Orrnob's Drop Automation
    Author  : Orrnob Mahmud
    Github  : https://github.com/OrrnobMahmud
    Telegram: https://t.me/verifiedcryptoairdops
    """ + Style.RESET_ALL)
    
    print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Total accounts: {total_accounts}")
    print(Fore.YELLOW + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

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

# Initialize UserAgent object
ua = UserAgent()

def login(decoded_data):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/login?lang=en_US"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": ua.random,  # Random UserAgent here
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

def data(cookie):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/summary?lang=en_US"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": ua.random,  # Random UserAgent here
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
    print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
          Fore.GREEN + f"Balance: " + Fore.WHITE + f"{balance}")
    return molecule

def tap(cookie, molecule):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/gold/increase?lang=en_US"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": ua.random,  # Random UserAgent here
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-request-with": "null",
        "Referer": "https://www.kucoin.com/miniapp/tap-game?inviterUserId=5496274031&rcode=QBSTAPN3",
        "cookie": cookie
    }

    total_increment = 0

    while total_increment < 3000 and running:
        increment = random.randint(55, 60)
        form_data = {
            'increment': str(increment),
            'molecule': str(molecule)
        }

        try:
            response = requests.post(url, headers=headers, data=form_data)
            total_increment += increment
            
            print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
                  Fore.GREEN + f"Tapped: " + Fore.WHITE + f"{increment} | " + 
                  Fore.GREEN + f"Total Tap: " + Fore.WHITE + f"{total_increment}/3000")
            
            time.sleep(2)
        except requests.exceptions.RequestException:
            print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
                  Fore.RED + "Network error occurred. Retrying...")
            time.sleep(5)

def new_balance(cookie):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/summary?lang=en_US"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": ua.random,  # Random UserAgent here
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
    print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
          Fore.GREEN + f"New Balance: " + Fore.WHITE + f"{balance}")

def main():
    global running

    clear_terminal()
    
    # File path
    file_path = os.path.join(os.path.dirname(__file__), "data.txt")

    # Read accounts from the file
    accounts = read_data_file(file_path)

    # Display the ASCII art and total accounts
    art(len(accounts))

    # Loop through each account
    for encoded_data in accounts:
        if not running:
            break

        # Decode account information
        decoded_data = decode_data(encoded_data)

        # Login and get the session cookie
        cookie = login(decoded_data)

        # Retrieve balance data and molecule ID
        molecule = data(cookie)

        # Perform the tap action
        tap(cookie, molecule)

        # Display new balance
        new_balance(cookie)

if __name__ == "__main__":
    main()

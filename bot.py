import time
import requests
import random
import urllib.parse
import os
from colorama import Fore, Style, init

# Initialize colorama for color output
init(autoreset=True)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Header visual from Blum Auto
def art():
    print("\033[1;96m" + r"""  ______   __               __     __     ____                              
 /      \ /  |             /  |   /  |   /    \                             
/$$$$$$  |$$/  _______  ___$$ |_  $$ |   $$$$  \   ______    ______         
$$ \__$$/ /  |/       \/   $$   |  $$ |   $$ $$  | /      \  /      \        
$$      \ $$ |$$$$$$$  $$$$$$  $$ |  $$ |  $$  $$< $$$$$$  |/$$$$$$  |      
 $$$$$$  |$$ |$$ | $$ | $$ |$$ $$   $$ |  $$$$  $$ $$    $$ $$    $$ |     
/  \__$$ |$$ |$$ | $$ | $$ | $$$$$$  $$ |__ $$ \ $$$$$$$$/$$$$$$$$/       
$$    $$ |$$ |$$ | $$ | $$ | $$$/   $$    $$ $$ $$    $$/ $$       |        
 $$$$$$$/ $$/ $$/  $$/  $$/  $$/    $$$$$$$/  $$$$$$$$/  $$$$$$$$/     
    """ + "\033[0m")
    print("\033[1;94m" + r""" __________                                                        
|          |                                                   
|____  ____|_________  _______________  ___      ______  
|    | |    \  /     \/      \  \     \ |      \  \__/  \
|    | |    \ |      \    |__/    \ |       \    \__/  \___/  
  |_____/______/_____/\____/______/_____/_/""" + "\033[0m\n")
    print("\033[1;95m" + "Powered by Orrnob Drop Automation\n" + "\033[0m")
    print("\033[1;96m" + "Github: https://github.com/OrrnobMahmud\n" + "\033[0m")

def countdown_timer(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        print(f"{Fore.CYAN + Style.BRIGHT}Wait {hours:02}:{mins:02}:{secs:02}", end='\r')
        time.sleep(1)
        seconds -= 1
    print("Wait 00:00:00          ", end='\r')

def countdown_timer(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        print(f"{Fore.CYAN + Style.BRIGHT}Wait {hours:02}:{mins:02}:{secs:02}", end='\r')
        time.sleep(1)
        seconds -= 1
    print("Wait 00:00:00          ", end='\r')

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

def main():
    file_path = "data.txt"
    encoded_data_list = read_data_file(file_path)
    
    while True:
        clear_terminal()
        art()
    
        for index, encoded_data in enumerate(encoded_data_list, start=1):
            print(f"{Fore.CYAN + Style.BRIGHT}------Account No.{index}------")
            decoded_data = decode_data(encoded_data)
            cookie = login(decoded_data)
            molecule = data(cookie)
            increment = random.randint(40, 60)
            tap(cookie, increment, molecule)
            new_balance(cookie)
            countdown_timer(2)
        countdown_timer(1*2*60)

if __name__ == "__main__":
    main()


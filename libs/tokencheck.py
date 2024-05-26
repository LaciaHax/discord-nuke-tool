import requests
import datetime
import time
from colorama import Fore

GREEN = Fore.GREEN
RED = Fore.RED
BLUE = Fore.BLUE
YELLOW = Fore.YELLOW

def check_token(token):
    while True:
        headers = {
            "Authorization": token
        }
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        if response.status_code == 200:
            print(f"{GREEN}[+] Token {token} is valid!")
            return True
        elif response.status_code == 429:
            print(f"{YELLOW}[!] ratelimited | {datetime.datetime.now()}")
            retry_after = int(response.headers.get('retry-after', 5)) + 5
            print(f"{YELLOW}[!] Sleeping for {retry_after} seconds")
            time.sleep(retry_after)
        else:
            print(f"{RED}[-] Token {token} is invalid!")
            return False

def remove_newline(token):
    return token.strip()

def main():
    token_path = "tokens.txt"
    dead_tokens = []

    with open(token_path, 'r') as file:
        tokens = file.read().splitlines()

    for token in tokens:
        if not check_token(token):
            dead_tokens.append(token)

    with open(token_path, 'w') as file:
        for token in tokens:
            if token not in dead_tokens:
                file.write(token + "\n")

    with open("dead_token.txt", "a") as file:
        for token in dead_tokens:
            file.write(token + "\n")

    print(f"{BLUE}[INFO] Dead tokens written to dead_token.txt")

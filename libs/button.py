import uuid
from tls_client import Session
import random
import threading
from colorama import Fore

GREEN = Fore.GREEN
RED = Fore.RED
BLUE = Fore.LIGHTBLUE_EX
YELLOW = Fore.YELLOW

def button_bypass(message: str, tokens: list, bot_id: str):
    try:
        access = []

        guild_id, channel_id, message_id = (
            message.split("/")[4],
            message.split("/")[5],
            message.split("/")[6],
         )

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

        for token in tokens:
            session.headers.update({"Authorization": token})
            site = session.get("https://discord.com")
            session.cookies = site.cookies
            params = {"around": message_id, "limit": 50}
            response = session.get(
                f"https://discord.com/api/v10/channels/{channel_id}/messages",
                params=params,
            )
            match response.status_code:
                case 200:
                    access.append(token)
                    break

        if not access:
            print("Missing permission :(")

        dictionary = []
        chosen = {}
        for msg in response.json():
            if msg.get("components", []):
                for component in msg["components"]:
                    for button in component["components"]:
                        if button.get("custom_id", {}):
                            custom_id = button["custom_id"]
                            dictionary.append(custom_id)

        for i, button in enumerate(dictionary, start=1):
            print(f"{i}: {button}")
        option = input("option: ")
        chosen[option] = button

        custom_id = chosen[option]

        def run_button(token):
            try:         
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
                json_data = {
                    "type": 3,
                    "guild_id": guild_id,
                    "channel_id": channel_id,
                    "message_flags": 0,
                    "message_id": message_id,
                    "application_id": bot_id,
                    "session_id": uuid.uuid4().hex,
                    "data": {
                        "component_type": 2,
                        "custom_id": custom_id,
                    },
                }
                response = session.post(
                    "https://discord.com/api/v10/interactions",
                    json=json_data,
                )
                match response.status_code:
                    case 204:
                        print(f"{GREEN}[+] Pressed")
                    case _:
                        print(f"{RED}[-] Failed")
            except Exception as e:
                print(f"{RED}[-] ERROR")

        threads = []
        for t in tokens:
            thread = threading.Thread(target=run_button, args=(t,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    except Exception as e:
        print("Failed sercg button")
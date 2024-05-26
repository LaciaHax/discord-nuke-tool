import random
import string
import threading
import time
import datetime
from tls_client import Session
from libs.solve import hCaptchaToken, OCR
from colorama import Fore

GREEN = Fore.GREEN
RED = Fore.RED
BLUE = Fore.BLUE
YELLOW = Fore.YELLOW

def rand_str(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def clean_invite(invite):
    return invite.replace("https://discord.gg/", "").replace("https://discord.com/invite/", "").replace("discord.gg/", "").replace("https://discord.com/invite/", "")

def joiner(token, invite):
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

    def join_with_token(token):
        session = Session(
            client_identifier=f"chrome_{random.randint(110, 115)}",
            random_tls_extension_order=True
        )
        session.headers.update(headers)

        ocr_solver = OCR("api.txt")

        if isinstance(invite, str):
            invites = [invite]
        else:
            invites = invite

        session.headers.update({"Authorization": token})
        site = session.get("https://discord.com")
        session.cookies = site.cookies

        for inv in invites:
            clean_code = clean_invite(inv)
            result = session.post(f"https://discord.com/api/v9/invites/{clean_code}", json={'session_id': rand_str(32)})
            status_code = result.status_code
            response_text = result.text

            if status_code == 200:
                status_message = f"{GREEN}[+] success :D"
                response_json = result.json()
                guild = response_json.get('guild_id', None)
                welcome_screen(token, guild)
            elif status_code == 400:
                print(f"{YELLOW}[!] need captcha {token[-12:]}")
                while True:
                    try:
                        result = session.post(f"https://discord.com/api/v9/invites/{clean_code}", json={'session_id': rand_str(32)})
                        status_code = result.status_code
                        if status_code == 429:
                            print(f"{YELLOW}[!] ratelimited | {datetime.datetime.now()}")
                            retry_after = int(result.headers.get('retry-after', 5)) + 5
                            print(f"{YELLOW}[!] Sleeping for {retry_after} seconds")
                            time.sleep(retry_after)
                            continue
                        error_json = result.json()
                        captcha_sitekey = error_json.get("captcha_sitekey")
                        captcha_rqdata = error_json.get("captcha_rqdata")
                        captcha_rqtoken = error_json.get("captcha_rqtoken")
                        captcha_payload = {
                            "type": "hcaptcha",
                            "url": "https://discord.com",
                            "sitekey": captcha_sitekey,
                            "rqdata": captcha_rqdata,
                            "rqtoken": captcha_rqtoken
                        }
                        token_solver = hCaptchaToken("api.txt")
                        token_solver.solve(captcha_payload)
                        if token_solver.solved:
                            session.headers.update({"X-Captcha-Key": token_solver.token})
                            session.headers.update({"X-Captcha-Rqtoken": captcha_rqtoken})
                            result = session.post(f"https://discord.com/api/v9/invites/{clean_code}", json={'session_id': rand_str(32)})
                            status_code = result.status_code
                            response_text = result.text
                            status_message = f"{GREEN}[+] solved {token[-12:]}"
                            status_message = f"{GREEN}[+] success :D"
                            response_json = result.json()
                            guild = response_json.get('guild_id', None)
                            welcome_screen(token, guild)
                            break
                    except Exception as e:
                        print(f"{RED}[-] Error while solving captcha: {e}")
            elif status_code == 429:
                print(f"{YELLOW}[!] ratelimited | {datetime.datetime.now()}")
                retry_after = int(result.headers.get('retry-after', 5)) + 5
                print(f"{YELLOW}[!] Sleeping for {retry_after} seconds")
                time.sleep(retry_after)
                join_with_token(token)
                return
            elif status_code == 500:
                status_message = f"{RED}[-] token is dead :P"
            else:
                status_message = f"{RED}[-] Unexpected status code: {status_code}"

            print(f"{status_message}\n{response_text}")
        
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
            data = resp.json()
            now = int(time.time() * 1000)

            for i in data["prompts"]:
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
                        resp = tls.post(f"https://discord.com/api/v10/guilds/{guild}/onboarding-responses", headers, data=json_data)
                        if resp == 200:
                            print(f"{GREEN}[+] Success bypass welcome-screen {token[-12:]}")
                        else:
                            print(f"{RED}[-] Failed to bypass welcome-screen {token[-12:]}")
                    else:
                        print(f"{GREEN}[+] no welcome-screen in this guild")

    if isinstance(token, str):
        tokens = [token]
    else:
        tokens = token

    threads = []
    for t in tokens:
        thread = threading.Thread(target=join_with_token, args=(t,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
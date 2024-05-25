import random
import string
import threading
import time
import json
import datetime
from tls_client import Session
from libs.solve import hCaptchaToken, OCR

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

            if status_code == 400:
                print(f"[*] need captcha {token}")
                while True:
                    try:
                        result = session.post(f"https://discord.com/api/v9/invites/{clean_code}", json={'session_id': rand_str(32)})
                        status_code = result.status_code
                        if status_code == 429:
                            print(f"[!] ratelimited | {datetime.datetime.now()}")
                            retry_after = int(result.headers.get('retry-after', 5)) + 5
                            print(f"[!] Sleeping for {retry_after} seconds")
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
                            status_message = f"[+] solved {token}"
                            break
                    except Exception as e:
                        print(f"Error while solving captcha: {e}")
            elif status_code == 200:
                status_message = "success :D"
            elif status_code == 429:
                print(f"[!] ratelimited | {datetime.datetime.now()}")
                retry_after = int(result.headers.get('retry-after', 5)) + 5
                print(f"[!] Sleeping for {retry_after} seconds")
                time.sleep(retry_after)
                join_with_token(token)
                return
            elif status_code == 500:
                status_message = "token is dead :P"
            else:
                status_message = f"Unexpected status code: {status_code}"

            print(f"{status_message}\n{response_text}")

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
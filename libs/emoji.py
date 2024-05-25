import requests
import time
import datetime
import threading
import random
import string
import re
import json
from libs.fetch import get_members

def is_channel_valid(token, channel_id):
    while True:
        headers = {
            "accept": "*/*",
            "authorization": token,
        }   
        response = requests.post(f"https://discord.com/api/v10/channels/{channel_id}/typing", headers=headers)
        print(f"{channel_id} trying ...")
        if response.status_code == 204:
            print(f"[+] Success {channel_id}")
            return response.status_code == 204
        elif response.status_code == 429:
            print(f"[!] ratelimited | {datetime.datetime.now()}")
            response_json = json.loads(response.text)
            retry_after = float(response_json['retry_after'])
            sleep_time = retry_after + 5
            print(f"[!] Sleeping for {sleep_time} seconds")
            time.sleep(sleep_time)
        else:
            print(f"[-] {response.status_code} faild {channel_id}")
            return response.status_code == 204

def get_valid_channels(server_id, token):
    headers = {
        "accept": "application/json",
        "authorization": token,
    }
    response = requests.get(f"https://discord.com/api/v10/guilds/{server_id}/channels", headers=headers)
    if response.status_code == 200:
        channels = [channel["id"] for channel in response.json() if is_channel_valid(token, channel["id"])]
        print(f"[INFO] channels | {channels}")
        return channels
    else:
        print("[-] Failed to get channel list.")
        return []

def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def generate_random_hiragana(length):
    hiragana_chars = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん'
    random_hiragana = ''.join(random.choice(hiragana_chars) for _ in range(length))
    return random_hiragana

def read_message_from_file(file_path):
    emoticons = [
    "✌","😂","😝","😁","😱","👉","🙌","🍻","🔥","🌈","☀","🎈","🌹","💄","🎀","⚽","🎾","🏁","😡","👿",
    "🐻","🐶","🐬","🐟","🍀","👀","🚗","🍎","💝","💙","👌","❤","😍","😉","😓","😳","💪","💩","🍸",
    "🔑","💖","🌟","🎉","🌺","🎶","👠","🏈","⚾","🏆","👽","💀","🐵","🐮","🐩","🐎","💣","👃",
    "👂","🍓","💘","💜","👊","💋","😘","😜","😵","🙏","👋","🚽","💃","💎","🚀","🌙","🎁","⛄",
    "🌊","⛵","🏀","🎱","💰","👶","👸","🐰","🐷","🐍","🐫","🔫","👄","🚲","🍉","💛","💚",
    "🤖","🦄","🎂","🎃","👻","💔","💤","💥","🍕","🍔","🍟","🍣","🍤","🍦","🍩","🍪","🎄","🎋",
    "🎍","🎎","🎓","🎤","🎧","🎮","🏆","🏅","🏵","🎗","🎫","🎭","🎨","🎰","🚂","🚃","🚄","🚅",
    "🚉","🚊","🚲","🛴","🛵","🛶","🛳","🛰","🛸","🛋","🛏","🛁","🛀","🕶","🕵","🕺","🖖","🖤",
    "🖥","🖨","🖱","🖲","🖼","🗂","🗃","🗄","🗑","🗒","🗓","🗜","🗝","🗞","🗡","🗣","🗯","🗳","🗺",
    "🗻","🗼","🗽","🗾","🗿","😀","😁","😂","😃","😄","😅","😆","😉","😊","😋","😎","😍","😘",
    "😗","😙","😚","😜","😝","😛","🤑","🤗","🤔","🤐","😷","🤒","🤕","🤢","🤧","😇","🤠","🤡",
    "🤥","🤫","🤭","🧐","🤓","😈","👿","👹","👺","💩","👻","💀","☠","👽","👾","🤖","😺","😸",
    "😹","😻","😼","😽","🙀","😿","😾","👐","🙌","👏","🤲","🤝","👍","👎","👊","✊","🤛","🤜",
    "🤞","✌","🤟","🤘","👌","👈","👉","👆","👇","☝","✋","🤚","🖐","🖖","👋","🤙","💪","🖕",
    "🙏","🦶","🦵","🦿","🦾","🧠","🦷","🦴","👂","👃","🧑","👶","🧒","👦","👧","🧔","👨",
    "🧔‍♂️","👩","🧔‍♀️","👱‍♂️","👱‍♀️","🧓","👴","👵","👲","👳‍♂️","👳‍♀️","🧕","👮‍♂️",
    "👮‍♀️","👷‍♂️","👷‍♀️","💂‍♂️","💂‍♀️","🕵️‍♂️","🕵️‍♀️","👩‍⚕️","👨‍⚕️","👩‍🌾","👨‍🌾",
    "👩‍🍳","👨‍🍳","👩‍🎓","👨‍🎓","👩‍🎤","👨‍🎤","👩‍🏫","👨‍🏫","👩‍🏭","👨‍🏭","👩‍💻","👨‍💻",
    "👩‍💼","👨‍💼","👩‍🔧","👨‍🔧","👩‍🔬","👨‍🔬","👩‍🎨","👨‍🎨","👩‍🚒","👨‍🚒","👩‍✈️","👨‍✈️",
    "👩‍🚀","👨‍🚀","👩‍⚖️","👨‍⚖️","👰","🤵","👸","🤴","🦸‍♀️","🦸‍♂️","🦹‍♀️","🦹‍♂️",
    "🤶","🎅","🧙‍♀️","🧙‍♂️","🧝‍♀️","🧝‍♂️","🧛‍♀️","🧛‍♂️","🧟‍♀️","🧟‍♂️","🧞‍♀️","🧞‍♂️",
    "🧜‍♀️","🧜‍♂️","🧚‍♀️","🧚‍♂️","👼","🤰","🤱","👩‍🍼","👨‍🍼","🙇‍♀️","🙇‍♂️","💁‍♀️",
    "💁‍♂️","🙅‍♀️","🙅‍♂️","🙆‍♀️","🙆‍♂️","🙋‍♀️","🙋‍♂️","🧏‍♀️","🧏‍♂️","🙎‍♀️",
    "🙎‍♂️","🙍‍♀️","🙍‍♂️","💇‍♀️","💇‍♂️","💆‍♀️","💆‍♂️","🧖‍♀️","🧖‍♂️","👩‍🦯",
    "👨‍🦯","👩‍🦼","👨‍🦼","👩‍🦽","👨‍🦽","🚶‍♀️","🚶‍♂️","🧍‍♀️","🧍‍♂️","🧎‍♀️","🧎‍♂️",
    "🏃‍♀️","🏃‍♂️","💃","🕺","🕴","👯‍♀️","👯‍♂️","🧖‍♀️","🧖‍♂️","🧗‍♀️","🧗‍♂️",
    "🧘‍♀️","🧘‍♂️","🛀","🛌","👭","👫","👬","💏","💑","👪","🗣","👤","👥","🫂",
    "👣","🐵","🐒","🦍","🦧","🐶","🐕","🦮","🐕‍🦺","🐩","🐺","🦊","🦝","🐱","🐈",
    "🦁","🐯","🐅","🐆","🐴","🐎","🦄","🦓","🦌","🦬","🐮","🐂","🐃","🐄","🐷",
    "🐖","🐗","🐽","🐏","🐑","🐐","🐪","🐫","🦙","🦒","🐘","🦣","🦏","🦛","🐭",
    "🐁","🐀","🐹","🐰","🐇","🐿","🦫","🦔","🦇","🐻","🐨","🐼","🦥","🦦","🦨",
    "🦘","🦡","🐾","🦃","🐔","🐓","🐣","🐤","🐥","🐦","🐧","🕊","🦅","🦆","🦢",
    "🦉","🦤","🪶","🦩","🦚","🦜","🦢","🦩","🦉","🦇","🦋","🐌","🐛","🐜","🐝",
    "🐞","🦗","🪳","🕷","🕸","🦂","🦟","🪰","🪲","🦠","💐","🌸","💮","🏵","🌹",
    "🥀","🌺","🌻","🌼","🌷","🌱","🪴","🌲","🌳","🌴","🌵","🌾","🌿","☘","🍀",
    "🍁","🍂","🍃","🍄","🌰","🦀","🦞","🦐","🦑","🐙","🐚","🐌","🦋","🐛","🐝",
    "🐜","🐞","🦂","🦗","🕷","🕸","🦂","🦞","🦀","🐍","🦎","🦕","🦖","🐢","🐊",
    "🐲","🐉","🐉","🦀","🦑","🐙","🐚","🪸","🐙","🐠","🐟","🐬","🐳","🦈","🐋",
    "🐊","🐅","🐆","🦓","🦍","🦏","🐪","🐫","🦙","🦒","🐘","🐑","🐏","🦌","🦬",
    "🦛","🦘","🦒","🦌","🐫","🐪","🐿","🦫","🦔","🦇","🦉","🦢","🦜","🦩","🦚",
    "🦝","🐾","🐉","🦀","🦞","🦐","🦑","🐙","🦀","🦑","🐠","🐟","🐡","🦈","🐋",
    "🐳","🦭","🐊","🐢","🦎","🐍","🦖","🦕","🦔","🦦","🦥","🦫","🦨","🦘","🦛",
    "🦏","🦓","🦍","🦧","🐶","🐕","🦮","🐩","🐺","🦊","🐱","🐈","🦁","🐯","🐅",
    "🐆","🐴","🐎","🦄","🦓","🦌","🦬","🐄","🐂","🐃","🐪","🐫","🐘","🦣","🦒",
    "🦘","🦛","🦏","🦍","🦧","🦣","🐘","🦏","🦛","🦣","🦥","🦦","🦨","🦫","🦡",
    "🦃","🐓","🐔","🐦","🕊","🦅","🦆","🦢","🦉","🦜","🦩","🦚","🦜","🦢","🦩",
    "🦉","🦜","🦩","🦚","🦉","🦜","🦩","🦚","🦉","🦩","🦉","🦩","🦚","🦩","🦉",
    "🦉"]
    
    with open(file_path, 'r') as file:
        cleaned_message = file.read()


    random_emoticons = random.choices(emoticons, k=256)
    emoji_string = ''.join(random_emoticons)
    modified_message = emoji_string + cleaned_message

    return modified_message

def send_message(token, channel_id, message):
    headers = {
        "accept": "*/*",
        "accept-language": "ja,en-US;q=0.9,en;q=0.8",
        "authorization": token,
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "ja",
        "x-discord-timezone": "Asia/Tokyo",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImphIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjYxOTczLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
    }
    data = {
        "content": message
    }
    response = requests.post(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers=headers, json=data)
    return response

def send_messages(tokens, server_id):
    if not isinstance(tokens, list):
        tokens = [tokens]
    delay = float(input("送信間隔を入力してください（s) > "))
    multi_channel_mode = input("Multi channel modeを有効にしますか？(y/n) >  ")
    
    channel_id = input("チャンネルIDを入力してください > ")
    
    print(f"[INFO] fetch members....")
    user_ids = get_members(tokens[0], server_id, channel_id)

    message = read_message_from_file("emoji_message.txt")
    if multi_channel_mode.lower() == 'y':
        print("[INFO] get_channels....")
        channels = get_valid_channels(server_id, tokens[0])

        def multi_mode(token):
            while True:
                for channel in channels:
                    modified_message = re.sub(r"{rand-(\d+)}", lambda x: generate_random_string(int(x.group(1))), message)
                    modified_message = re.sub(r"{randjp-(\d+)}", lambda x: generate_random_hiragana(int(x.group(1))), modified_message)
                    modified_message = modified_message.replace("{ghost}", "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||||||||||")
                    while "{randmen}" in modified_message:
                        mention = f"<@{random.choice(user_ids)}>"
                        modified_message = modified_message.replace("{randmen}", mention, 1)
                    res = send_message(token, channel, modified_message)
                    status_code = res.status_code
                    if status_code == 429:
                        print(f"[!] ratelimited | {datetime.datetime.now()}")
                        response_json = json.loads(res.text)
                        retry_after = float(response_json['retry_after'])
                        sleep_time = retry_after + 5
                        print(f"[!] Sleeping for {sleep_time} seconds")
                        time.sleep(sleep_time)
                    elif status_code == 200 or 204:
                        print(f"[+] Success send {token} {channel}")
                        time.sleep(delay)
                    else:
                        print(f"[-] Failed send {token} {channel}")

        threads = []
        for token in tokens:
            thread = threading.Thread(target=multi_mode, args=(token,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    elif multi_channel_mode.lower() == 'n':
        def single_mode(token):
            while True:
                modified_message = re.sub(r"{rand-(\d+)}", lambda x: generate_random_string(int(x.group(1))), message)
                modified_message = re.sub(r"{randjp-(\d+)}", lambda x: generate_random_hiragana(int(x.group(1))), modified_message)
                modified_message = modified_message.replace("{ghost}", "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||||||||||")
                while "{randmen}" in modified_message:
                    mention = f"<@{random.choice(user_ids)}>"
                    modified_message = modified_message.replace("{randmen}", mention, 1)
                res = send_message(token, channel_id, modified_message)
                status_code = res.status_code
                if status_code == 429:
                    print(f"[!] ratelimited | {datetime.datetime.now()}")
                    response_json = json.loads(res.text)
                    retry_after = float(response_json['retry_after'])
                    sleep_time = retry_after + 5
                    print(f"[!] Sleeping for {sleep_time} seconds")
                    time.sleep(sleep_time)
                elif status_code == 200 or 204:
                    print(f"[+] Success send {token} {channel_id}")
                    time.sleep(delay)
                else:
                    print(f"[-] Failed send {token} {channel_id}")

        threads = []
        for token in tokens:
            thread = threading.Thread(target=single_mode, args=(token,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
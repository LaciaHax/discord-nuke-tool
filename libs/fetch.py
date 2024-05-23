import random
import sys
import json
import websocket
import requests

def fetch_user_ids(token, guild, channel):
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
    heartbeat_interval = json.loads(ws.recv())['d']['heartbeat_interval']

    ws.send(
        json.dumps(
            {
                "op": 2,
                "d": {
                    "token": token,
                    "properties": {
                        "$os": "windows",
                        "$browser": "Discord",
                        "$device": "desktop"
                    }
                }
            }
        )
    )

    ws.send(
        json.dumps(
            {
                "op": 14,
                "d": {
                    "guild_id": guild,
                    "typing": True,
                    "threads": False,
                    "activities": True,
                    "members": [],
                    "channels": {channel: [[0, 99]]}
                }
            }
        )
    )

    received_data = ws.recv()
    json_data = json.loads(received_data)

    guilds = json_data['d']['guilds']

    for guild in guilds:
        if guild["id"] == '956638414424387615':
            for member in guild["members"]:
                print(member["user"]["id"])

    ws.send(
        json.dumps(
            {
                "op": 14,
                "d": {
                    "guild_id": guild,
                    "channels": {channel: [[0, 99], [100, 199]]}
                }
            }
        )
    )

    received_data = ws.recv()
    json_data = json.loads(received_data)

    user_ids = []
    for item in json_data['d']['ops'][0]['items']:
        if 'member' in item:
            user_id = item['member']['user']['id']
            user_ids.append(user_id)

    return user_ids
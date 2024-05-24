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
    if 'ops' in json_data['d']:
        for item in json_data['d']['ops']:
            if 'items' in item:
                for member in item['items']:
                    if 'member' in member:
                        user_id = member['member']['user']['id']
                        user_ids.append(user_id)

    return user_ids
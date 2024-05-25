import json
import websocket
import time

def get_members(token, server, channel):
    ws = websocket.create_connection("wss://gateway.discord.gg/?v=10&encoding=json")
    users = []
    while True:
        msg = json.loads(ws.recv())
        if msg["t"] is None:
            ws.send(json.dumps({"op": 2, "d": {"token": token, "capabilities": 16381, "properties": {"os": "Android", "browser": "Discord Android", "device": "Android", "system_locale": "ja-JP", "browser_user_agent": "Discord-Android/223015", "browser_version": "", "os_version": "", "referrer": "", "referring_domain": "", "referrer_current": "", "referring_domain_current": "", "release_channel": "stable", "client_build_number": 223015, "client_event_source": None}, "presence": {"status": "invisible", "since": 0, "activities": [], "afk": False}, "compress": False, "client_state": {"guild_versions": {}, "highest_last_message_id": "0", "read_state_version": 0, "user_guild_settings_version": -1, "private_channels_version": "0", "api_code_version": 0}}}))
        elif msg["t"] == "READY_SUPPLEMENTAL":
            ws.send(json.dumps({"op": 14, "d": {"guild_id": server, "typing": True, "activities": True, "threads": True, "channels": {channel: [[0, 99]]}}}))
        elif msg["t"] == "GUILD_MEMBER_LIST_UPDATE":
            for item in msg["d"]["ops"]:
                if item["op"] == "SYNC":
                    for i in item["items"]:
                        if "member" in i:
                            users.append(i["member"]["user"]["id"])
                    ws.close()
                    return users
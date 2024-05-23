import requests

def leave_server(tokens, id):
    if not isinstance(tokens, list):
        tokens = [tokens]

    url = f"https://discord.com/api/v9/users/@me/guilds/{id}"
    
    for token in tokens:
        headers = {
            'Authorization': f'{token}'
        }

        payload = {
            'lurking': False,
        }

        response = requests.delete(url, headers=headers, data=payload)
        
        if response.status_code == 204:
            print(f"退出しました。 {id}  {token}.")
        else:
            print(f"失敗しました。 {id}  {token} {response.status_code}")
            print(response.text)
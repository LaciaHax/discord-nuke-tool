import requests

def check_token(token):
    headers = {
        "Authorization": token
    }
    response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    if response.status_code == 200 or 204:
        print(f"[+] Token {token} is valid!")
        return True
    elif response.status_code == 429:
        print(f"[!] Token {token} rate limited. Ignoring...")
        return True
    else:
        print(f"[-] Token {token} is invalid!")
        return False

def remove_newline(token):
    return token.strip()

def main():
    token_path = "tokens.txt"
    dead_tokens = []

    with open(token_path, 'r') as file:
        tokens = file.read().splitlines()

    for token in tokens:
        if not check_token(token):
            dead_tokens.append(token)

    with open(token_path, 'w') as file:
        for token in tokens:
            if token not in dead_tokens:
                file.write(token + "\n")

    with open("dead_token.txt", "a") as file:
        for token in dead_tokens:
            file.write(token + "\n")

    print("Dead tokens written to dead_token.txt")

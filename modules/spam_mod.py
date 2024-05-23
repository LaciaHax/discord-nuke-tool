from libs.spam import send_messages

token_path = "tokens.txt"

with open(token_path, 'r') as file:
    tokens = file.read().splitlines()

def spam_mod():
    server_id = input("サーバーID > ")
    send_messages(tokens, server_id)
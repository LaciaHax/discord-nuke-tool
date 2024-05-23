from libs.leave import leave_server

token_path = "tokens.txt"

with open(token_path, 'r') as file:
    tokens = file.read().splitlines()

def leave_mod():
    svid = input("サーバーID > ")
    leave_server(tokens, svid)
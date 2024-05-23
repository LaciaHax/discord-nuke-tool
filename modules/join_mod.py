from libs.invite import joiner

token_path = "tokens.txt"

with open(token_path, 'r') as file:
    tokens = file.read().splitlines()

def join_mod():
    invite = input("input invite url > ")
    print("joining...")
    joiner(tokens, invite)
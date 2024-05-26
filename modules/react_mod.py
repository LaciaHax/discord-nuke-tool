from libs.reaction import react_emoji

token_path = "tokens.txt"

with open(token_path, 'r') as file:
    tokens = file.read().splitlines()

def add_emoji():
    react_emoji(tokens)
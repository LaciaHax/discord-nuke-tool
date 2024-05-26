from libs.welcome import welcome_screen

token_path = "tokens.txt"

with open(token_path, 'r') as file:
    tokens = file.read().splitlines()

def welcome_mod():
    guild = input("guild id > ")
    for token in tokens:
        welcome_screen(token, guild)
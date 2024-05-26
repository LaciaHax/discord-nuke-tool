from libs.button import button_bypass

token_path = "tokens.txt"

with open(token_path, 'r') as file:
    tokens = file.read().splitlines()

def button():
    message = input("message url > ")
    bot = input("bot-id > ")
    button_bypass(message, tokens, bot)
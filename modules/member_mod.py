from libs.member import accept_rules

token_path = "tokens.txt"

with open(token_path, 'r') as file:
    tokens = file.read().splitlines()

def rule():
    guild = input("Guild ID > ")
    accept_rules(guild, tokens)
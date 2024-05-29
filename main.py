import os
import time
from visuals.options import show
from modules.join_mod import join_mod
from modules.leave_mod import leave_mod
from modules.spam_mod import spam_mod
from modules.token_mod import token_mod
from modules.emoji_mod import emoji_mod
from modules.react_mod import add_emoji
from modules.butotn_mod import button
from modules.welcome_mod import welcome_mod
from modules.member_mod import rule
from colorama import Fore

lists = [
    join_mod,
    leave_mod,
    spam_mod,
    token_mod,
    emoji_mod,
    add_emoji,
    button,
    welcome_mod,
    rule,
]

while True:
    os.system('cls')
    show()
    choice = int(input("what is your choise > "))
    if 1 <= choice <= len(lists):
        os.system('cls')
        lists[choice - 1]()
    else:
        print("you cant read options????")
        time.sleep(3)
    time.sleep(3)
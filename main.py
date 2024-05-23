import os
import time
from visuals.options import show
from modules.join_mod import join_mod
from modules.leave_mod import leave_mod
from modules.spam_mod import spam_mod
from modules.token_mod import token_mod

lists = [
    join_mod,
    leave_mod,
    spam_mod,
    token_mod,
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
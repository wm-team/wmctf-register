import sys
from os import system, environ

from app import main_app
from menu import MainMenu, run_menu

system("echo 'Welcome to WMCTF 2022' | figlet -f slant -c -t | lolcat")

difficulty = int(environ.get("POW_DIFFICULTY", "0"))

r = system(f"python3 pow.py ask {difficulty}")
if r != 0:
    print("Failed to start pow")
    sys.exit(1)

main_app.init_db()

run_menu(MainMenu())

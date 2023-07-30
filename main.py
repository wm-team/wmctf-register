import sys
from os import system, environ

from app.app import App
from config import INTRODUCTION
from menu.MainMenu import MainMenu

if not environ.get("DEBUG"):
    system("echo 'Welcome to WMCTF 2023' | figlet -f lean -c -t | lolcat")

    difficulty = int(environ.get("POW_DIFFICULTY", "0"))

    r = system(f"python3 pow.py ask {difficulty}")
    if r != 0:
        print("Failed to start pow")
        sys.exit(1)

    print(INTRODUCTION)

app = App()
app.run_menu(MainMenu.this())

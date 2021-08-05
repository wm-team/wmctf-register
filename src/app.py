#!/usr/bin/env python3
import subprocess

import traceback

from db import User, session
from region import get_region_name


def register():
    teamname = input("Team name: ")
    email = input("Email: ")
    phone = input("Phone(we won't tell anyone): ")
    password = input("Password: ")
    repassword = input("Re-type Password: ")
    location = input(
        "Location(Country/Region Code, https://en.wikipedia.org/wiki/ISO_3166-1): ").upper()
    if password != repassword:
        print("Passwords do not match.")
        return
    try:
        user = User.register(teamname, email, phone, password, location)
    except Exception as e:
        print(','.join(e.args))
        exit(1)
    user.send_verify_email()
    print(f"We have sent a verify email to {email}, go and check it!\n")
    verify(user.teamname, user.password)


def verify(teamname=None, password=None):
    if not teamname:
        teamname = input("Team name: ")
    if not password:
        password = input("Password: ")
    code = input("Enter the code: ")
    try:
        user = User.login(teamname, password)
    except Exception as e:
        print(','.join(e.args))
        exit(1)
    if user.verify(code):
        print("Verified!")
    session.commit()
    check(user.teamname, user.password)


def check(teamname=None, password=None):
    if not teamname:
        teamname = input("Team name: ")
    if not password:
        password = input("Password: ")
    try:
        user = User.login(teamname, password)
    except Exception as e:
        print(','.join(e.args))
        exit(1)
    if user.verified:
        print(
            f"Welcome, {user.teamname}! You have successfully register for W&M CTF.")
        print(f"Team name: {user.teamname}")
        print(f"Email: {user.email}")
        print(f"Phone: {user.phone}")
        print(f"Location: {user.location} {get_region_name(user.location)}")
    else:
        print("Welcome, {user.teamname}! You need to verify first.")
        print(f"Go and check your email {user.email}.")


def resend(teamname=None, password=None):
    if not teamname:
        teamname = input("Team name: ")
    if not password:
        password = input("Password: ")
    try:
        user = User.login(teamname, password)
    except Exception as e:
        print(','.join(e.args))
        exit(1)
    user.send_verify_email()
    print(f"We have resent a verify email to {user.email}, go and check it!\n")
    verify(user.teamname, user.password)


def forget(email=None):
    if not email:
        email = input("Email: ")
    try:
        user = User.find_by_email(email)
        if user:
            user.send_forget_email()
    except Exception as e:
        pass  # do not notify when not exists, prevent enumeration
    print(f"We have resent a forget email to {email}, go and check it!\n")


if __name__ == "__main__":
    try:
        subprocess.check_call(
            ["python3", "pow.py", "ask", "31337"], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print("Wrong pow.")
        exit(1)
    subprocess.check_call(
        "figlet 'Welcome To W&M CTF!' -w 1000| lolcat", shell=True)
    r = input("""Choose your action:
  1. register
  2. verify email
  3. check status
  4. resend email
  5. forget teamname/password
> """)
    try:
        if r == "1":
            register()
        elif r == "2":
            verify()
        elif r == "3":
            check()
        elif r == "4":
            resend()
        elif r == "5":
            forget()
        else:
            print("Wrong action.")
    except Exception as e:
        print("Something wrong happened")
        print("Please report to https://github.com/wm-team/wmctf-register/issues")
        traceback.print_exc()
        

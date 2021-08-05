#!/usr/bin/env python3
import subprocess

import sqlalchemy

from db import User, session
from region import get_region_name

def register():
    username = input("Team name: ")
    email = input("Email: ")
    phone = input("Phone(we won't tell anyone): ")
    password = input("Password: ")
    repassword = input("Re-type Password: ")
    location = input("Location(Country/Region Code, https://en.wikipedia.org/wiki/ISO_3166-1): ").upper()
    if password != repassword:
        print("Passwords do not match.")
        return
    user = User(username, email, phone, password, location)
    try:
        session.add(user)
        session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        key = e.orig.args[1].split("'")[-2]
        if key == "username":
            key = "team name"
        print(f"User already taken, {key} duplicated.")
        exit(1)
    except Exception:
        print("Invalid user information")
        exit(1)
    user.send_verify_email()
    print(f"We have sent a verify email to {email}, go and check it!\n")
    verify(user.username, user.password)

def verify(username=None, password=None):
    if not username:
        username = input("Team name: ")
    if not password:
        password = input("Password: ")
    code = input("Enter the code: ")
    user: User = session.query(User).filter(User.username==username,User.password==password).first()
    if not user:
        print(f"User {username} does not exist or wrong password.")
    if user.verify(code):
        print("Verified!")
    session.commit()
    check(user.username, user.password)

def check(username=None, password=None):
    if not username:
        username = input("Team name: ")
    if not password:
        password = input("Password: ")
    user: User = session.query(User).filter(User.username==username,User.password==password).first()
    if not user:
        print(f"User {username} does not exist or wrong password.")
    elif user.verified:
        print(f"Welcome, {user.username}! You have successfully register for W&M CTF.")
        print(f"Team name: {user.username}")
        print(f"Email: {user.email}")
        print(f"Phone: {user.phone}")
        print(f"Location: {user.location} {get_region_name(user.location)}")
    else:
        print("Welcome, {user.username}! You need to verify first.")
        print(f"Go and check your email {user.email}.")

def resend(username=None, password=None):
    if not username:
        username = input("Team name: ")
    if not password:
        password = input("Password: ")
    user: User = session.query(User).filter(User.username==username,User.password==password).first()
    if not user:
        print(f"User {username} does not exist or wrong password.")
    user.send_verify_email()
    print(f"We have resent a verify email to {user.email}, go and check it!\n")
    verify(user.username, user.password)

def forget(email=None):
    if not email:
        email = input("Email: ")
    user: User = session.query(User).filter(User.email==email).first()
    if user:
        user.send_forget_email()
    print(f"We have resent a forget email to {email}, go and check it!\n")

if __name__ == "__main__":
    try:
        subprocess.check_call(["python3", "pow.py", "ask", "31337"], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print("Wrong pow.")
        # exit(1)
    r = input("""Choose your action:
  1. register
  2. verify email
  3. check status
  4. resend email
  5. forget username/password
> """)
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
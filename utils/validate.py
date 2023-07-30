import re


def validate_name(name: str):
    return name.isprintable() and 3 <= len(name) <= 20


def validate_password(password: str):
    return password.isprintable() and 8 <= len(password) <= 20

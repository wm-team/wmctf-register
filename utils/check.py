import re

MAIL_RE = re.compile(
    r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
PHONE_RE = re.compile(
    r"^\s*(?:\+?(\d{1,3}))?([-. (]*(\d{3})[-. )]*)?((\d{3})[-. ]*(\d{2,4})(?:[-.x ]*(\d+))?)\s*$")


def check_email(email: str):
    return MAIL_RE.fullmatch(email)


def check_phone(phone: str):
    return PHONE_RE.fullmatch(phone)


def check_name(name: str):
    return name.isprintable() and 6 <= len(name) <= 20


def check_password(password: str):
    return password.isprintable() and 8 <= len(password) <= 20


def check_team_name(name: str):
    return name.isprintable() and 1 <= len(name) <= 20

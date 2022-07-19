import secrets


def random_string():
    return secrets.token_urlsafe()

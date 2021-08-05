import os

SQLALCHEMY_DATABASE_URI = "sqlite:///data/db.db"
MAIL_SERVER = "***"
MAIL_PORT = 25
MAIL_USERNAME = "***"
MAIL_DEFAULT_SENDER = "***"
MAIL_PASSWORD = "***"

for k in os.environ:
    globals()[k] = os.environ[k]
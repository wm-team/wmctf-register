import os

SQLALCHEMY_DATABASE_URI = "sqlite:///data/db.db"
DB_HASHED_PASSWORD = 1
MAIL_SERVER = "***"
MAIL_PORT = 25
MAIL_USERNAME = "***"
MAIL_DEFAULT_SENDER = "***"
MAIL_PASSWORD = "***"
MAIL_ASYNC = 0

for k in os.environ:
    globals()[k] = os.environ[k]
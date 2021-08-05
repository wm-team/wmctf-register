from sqlalchemy.ext.declarative import declarative_base
from config import SQLALCHEMY_DATABASE_URI
from mail import send_forget_email, send_verify_email
from region import is_valid_region_code
from sqlalchemy import create_engine
import sqlalchemy as sa
from sqlalchemy import orm
import random
import string

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
Base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(80), unique=True, nullable=False)
    email = sa.Column(sa.String(120), unique=True, nullable=False)
    password = sa.Column(sa.String(120), nullable=False)
    phone = sa.Column(sa.String(20), unique=True, nullable=False)
    location = sa.Column(sa.String(2), nullable=False)
    verify_code = sa.Column(sa.String(8), nullable=False)
    verified = sa.Column(sa.Boolean(), default=False)

    def __init__(self, username: str, email: str, phone: str, password: str, location: str):
        self.username = username
        self.email = email
        self.password = password
        self.location = location
        self.phone = phone
        self.verify_code = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(8))
        if not is_valid_region_code(self.location):
            print("Invalid region code")
            exit(1)

    def send_verify_email(self):
        send_verify_email(self.username, self.email, self.verify_code)
    
    def send_forget_email(self):
        send_forget_email(self.username, self.email, self.password)

    def verify(self, code: str):
        if self.verify_code == code:
            self.verified = True
        return self.verified

    def __repr__(self):
        return '<User %r>' % self.username

Base.metadata.create_all()
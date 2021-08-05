from sqlalchemy.ext.declarative import declarative_base
from config import DB_HASHED_PASSWORD, SQLALCHEMY_DATABASE_URI
from mail import send_forget_email, send_verify_email
from region import is_valid_region_code
from sqlalchemy import create_engine
import sqlalchemy as sa
from sqlalchemy import orm
import random
import string
import hashlib
import re

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
Base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)

MAIL_RE = re.compile(
    r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
PHONE_RE = re.compile(
    r"^\s*(?:\+?(\d{1,3}))?([-. (]*(\d{3})[-. )]*)?((\d{3})[-. ]*(\d{2,4})(?:[-.x ]*(\d+))?)\s*$")


class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    teamname = sa.Column(sa.String(80), unique=True, nullable=False)
    email = sa.Column(sa.String(120), unique=True, nullable=False)
    password = sa.Column(sa.String(120), nullable=False)
    phone = sa.Column(sa.String(20), unique=True, nullable=False)
    location = sa.Column(sa.String(2), nullable=False)
    verify_code = sa.Column(sa.String(8), nullable=False)
    verified = sa.Column(sa.Boolean(), default=False)

    def __init__(self, teamname: str, email: str, phone: str, password: str, location: str):
        self.teamname = teamname
        self.email = email
        if DB_HASHED_PASSWORD:
            self.password = hashlib.md5(password.encode()).hexdigest()
        else:
            self.password = password
        self.location = location
        self.phone = phone
        self.verify_code = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(8))
        self.check()

    def check(self):
        if not MAIL_RE.fullmatch(self.email):
            raise Exception("Invalid email")
        if not PHONE_RE.fullmatch(self.phone):
            raise Exception("Invalid phone")
        if not is_valid_region_code(self.location):
            raise Exception("Invalid region code")

    @staticmethod
    def login(teamname: str, password: str):
        if DB_HASHED_PASSWORD:
            password = hashlib.md5(password.encode()).hexdigest()
        user: User = session.query(User).filter(
            User.teamname == teamname, User.password == password).first()
        return user

    @staticmethod
    def register(teamname: str, email: str, phone: str, password: str, location: str):
        user = User(teamname, email, phone, password, location)
        try:
            session.add(user)
            session.commit()
        except sa.exc.IntegrityError as e:
            key = e.orig.args[1].split("'")[-2]
            raise Exception(f"User already taken, {key} duplicated.")
        except Exception as e:
            raise Exception("Invalid user information")
        return user

    @staticmethod
    def find_by_email(email: str):
        user = session.query(User).filter(User.email == email).first()
        return user

    def send_verify_email(self):
        send_verify_email(self.teamname, self.email, self.verify_code)

    def send_forget_email(self):
        send_forget_email(self.teamname, self.email, self.password)

    def verify(self, code: str):
        if self.verify_code == code:
            self.verified = True
        return self.verified

    def __repr__(self):
        return '<User %r>' % self.teamname


Base.metadata.create_all()

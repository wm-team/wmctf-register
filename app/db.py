import secrets
from typing import cast

import psycopg2
from passlib.hash import bcrypt_sha256

from config import config


class DB:
    __db: "DB"

    def __init__(self, url: str):
        self.conn = psycopg2.connect(url)

    def create_user(self, name: str, email: str, country: str | None, password: str) -> int:
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO users (name, email, country, password, hidden, banned, verified) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                        (name, email, country, bcrypt_sha256.hash(password), False, False, False))
            self.conn.commit()
            return cast(tuple, cur.fetchone())[0]

    def login_user(self, name: str, password: str) -> int:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, password FROM users WHERE name = %s", (name,))
            row=cur.fetchone()
            if row is None:
                return -1
            uid, hashed=row
            if bcrypt_sha256.verify(password, hashed):
                return uid
            else:
                return -1

    def create_team(self, name: str, password: str, captain_id: int) -> int:
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO teams (name, password, captain_id, secret, hidden, banned) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                        (name, bcrypt_sha256.hash(password), captain_id, secrets.token_urlsafe(), False, False))
            self.conn.commit()
            return cast(tuple, cur.fetchone())[0]

    def login_team(self, name: str, password: str) -> int:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, password FROM teams WHERE name = %s", (name,))
            row=cur.fetchone()
            if row is None:
                return -1
            uid, hashed=row
            if bcrypt_sha256.verify(password, hashed):
                return uid
            else:
                return -1

    def join_team(self, uid: int, tid: int) -> None:
        with self.conn.cursor() as cur:
            cur.execute("UPDATE users SET team_id = %s WHERE id = %s",
                        (tid, uid))
            self.conn.commit()

    def leave_team(self, uid: int) -> None:
        with self.conn.cursor() as cur:
            cur.execute("UPDATE users SET team_id = NULL WHERE id = %s", (uid,))
            self.conn.commit()

    def list_team(self, tid: int):
        with self.conn.cursor() as cur:
            cur.execute("SELECT name FROM users WHERE team_id = %s", (tid,))
            res = cur.fetchall()
            return [x[0] for x in res]

    @ classmethod
    def get_db(cls):
        db=getattr(cls, "__db", None)
        if db is None:
            cls.__db=DB(str(config.database))
        return cls.__db

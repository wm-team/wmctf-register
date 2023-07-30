import inquirer
from email_validator import validate_email
from pydantic import BaseModel
from rich import print

import utils.region as region
import utils.validate as validate

from .db import DB
from .team import Team


class User(BaseModel):
    id: int
    name: str
    team_id: int | None
    email: str
    country: str | None
    team: Team | None

    def join_team(self, tid: int):
        DB.get_db().join_team(self.id, tid)
        self.team_id = tid
        self.team = Team.load(tid)

    def leave_team(self):
        DB.get_db().leave_team(self.id)
        self.team_id = None
        self.team = None

    @staticmethod
    def load(id: int):
        with DB.get_db().conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (id,))
            res = cur.fetchone()
            assert res is not None, "User not found"
            return User(
                id=res[0],
                name=res[2],
                email=res[4],
                team_id=res[14],
                country=res[9],
                team=Team.load(res[14]) if res[14] is not None else None,
            )

    @staticmethod
    def check_username(username: str) -> bool:
        with DB.get_db().conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE name = %s", (username,))
            return cur.fetchone() is None

    @staticmethod
    def check_email(email: str) -> bool:
        with DB.get_db().conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
            return cur.fetchone() is None

    @staticmethod
    def register():
        def _validate_email(_, email):
            try:
                validate_email(email)
                return User.check_email(email)
            except:
                return False
        questions = [
            inquirer.Text('name', message="What's your name?", validate=lambda _,
                          x: validate.validate_name(x) and User.check_username(x)),
            inquirer.Text('email', message="What's your email?",
                          validate=_validate_email),
            inquirer.List('country', message="What's your country/region?",
                          choices=region.region_code, default="N/A"),
            inquirer.Password('password', message="What's your password?",
                              validate=lambda _, x: validate.validate_password(x)),
        ]
        answers = inquirer.prompt(questions)
        if answers:
            answers["country"] = answers["country"].split(" - ")[0]
            if answers["country"] == "N/A":
                answers["country"] = None
            return User.load(DB.get_db().create_user(**answers))

    @staticmethod
    def login():
        questions = [
            inquirer.Text('name', message="What's your name?"),
            inquirer.Password('password', message="What's your password?"),
        ]
        answers = inquirer.prompt(questions)
        if answers:
            id = DB.get_db().login_user(**answers)
            if id != -1:
                return User.load(id)
            else:
                print("User not found or password is incorrect.")
                return None

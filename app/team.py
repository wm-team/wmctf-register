import inquirer
from pydantic import BaseModel
from rich import print

import utils.validate as validate

from .db import DB


class Team(BaseModel):
    id: int
    name: str
    captain_id: int

    def list_members(self) -> list[str]:
        return DB.get_db().list_team(self.id)

    @staticmethod
    def load(id: int):
        with DB.get_db().conn.cursor() as cur:
            cur.execute("SELECT * FROM teams WHERE id = %s", (id,))
            res = cur.fetchone()
            assert res is not None, "User not found"
            return Team(
                id=res[0],
                name=res[2],
                captain_id=res[-1],
            )

    @staticmethod
    def check_teamname(username: str) -> bool:
        with DB.get_db().conn.cursor() as cur:
            cur.execute("SELECT 1 FROM teams WHERE name = %s", (username,))
            return cur.fetchone() is None

    @staticmethod
    def register(captain_id):
        questions = [
            inquirer.Text('name', message="What's your team name?", validate=lambda _,
                          x: validate.validate_name(x) and Team.check_teamname(x)),
            inquirer.Password('password', message="What's your team password?",
                              validate=lambda _, x: validate.validate_password(x)),
        ]
        answers = inquirer.prompt(questions)
        if answers:
            return Team.load(DB.get_db().create_team(**answers, captain_id=captain_id))

    @staticmethod
    def login():
        questions = [
            inquirer.Text('name', message="What's your name?"),
            inquirer.Password('password', message="What's your password?"),
        ]
        answers = inquirer.prompt(questions)
        if answers:
            id = DB.get_db().login_team(**answers)
            if id != -1:
                return Team.load(id)
            else:
                print("User not found or password is incorrect.")
                return None

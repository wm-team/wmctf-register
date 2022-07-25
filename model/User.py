from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app import DB

from .Team import Team


class User(DB.Base):
    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(80), unique=True, nullable=False)
    team_id = sa.Column(sa.Integer, sa.ForeignKey('team.id'))
    email = sa.Column(sa.String(120), nullable=False)
    password = sa.Column(sa.String(120), nullable=False)
    phone = sa.Column(sa.String(20), nullable=False)
    time_created = sa.Column(sa.DateTime(timezone=True),
                             server_default=func.now())

    def __init__(self, name: str, password: str, email: str, phone: str):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone

    @staticmethod
    def register(session: Session, name: str, email: str, phone: str, password: str):
        if User.get_by_name(session, name):
            return None
        user = User(
            name=name,
            email=email,
            phone=phone,
            password=password,
        )
        session.add(user)
        session.commit()
        return user

    @staticmethod
    def get_by_name(session: Session, email: str):
        return session.query(User).filter(User.name == email).first()

    @staticmethod
    def login(session: Session, name: str, password: str):
        user = User.get_by_name(session, name)
        if user and user.password == password:
            return user
        return None

    def my_team(self, session: Session):
        if self.team_id is None:
            return None
        return Team.get_by_id(session, int(str(self.team_id)))

    def exit_team(self, session: Session):
        self.team_id = None
        session.add(self)
        session.commit()

    def join_team(self, session: Session, token: str):
        team = Team.get_by_token(session, token)
        if not team:
            return None
        if len(session.query(User).filter(User.team_id == self.team_id).all()) >= 20:
            return "Team is full, please create a new team"
        self.team_id = team.id
        session.add(self)
        session.commit()
        return team

    def create_team(self, session: Session, name: str):
        team = Team.create(session, name)
        if not team:
            return None
        self.team_id = team.id
        session.add(self)
        session.commit()
        return team

    def team_status(self, session: Session):
        team = self.my_team(session)
        if not team:
            return "Not in team"
        return f"In team {team.name}"

    def teammates(self, session: Session) -> List["User"]:
        return session.query(User).filter(User.team_id == self.team_id).all()

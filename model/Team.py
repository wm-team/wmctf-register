from typing import Optional
import sqlalchemy as sa
from sqlalchemy.orm import Session
import datetime

from app import DB
from utils import random_string


class Team(DB.Base):
    __tablename__ = "team"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(80), unique=True, nullable=False)
    token = sa.Column(sa.String(80), unique=False, nullable=False)
    time_created = sa.Column(sa.DateTime(timezone=True), default=datetime.datetime.now)


    @staticmethod
    def create(session: Session, name: str) -> Optional["Team"]:
        if Team.get_by_name(session, name):
            return None
        team = Team(
            name=name,
            token=random_string(),
        )
        session.add(team)
        session.commit()
        return team

    @staticmethod
    def get_by_id(session: Session, id: int) -> Optional["Team"]:
        return session.query(Team).filter(Team.id == id).first()

    @staticmethod
    def get_by_name(session: Session, name: str) -> Optional["Team"]:
        return session.query(Team).filter(Team.name == name).first()

    @staticmethod
    def get_by_token(session: Session, token: str) -> Optional["Team"]:
        return session.query(Team).filter(Team.token == token).first()

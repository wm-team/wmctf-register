import os

from pydantic import BaseModel


class Config(BaseModel):
    database = os.environ.get("DATABASE_URL", "sqlite:///data/db.sqlite")

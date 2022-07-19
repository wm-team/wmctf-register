from os import path
from typing import TYPE_CHECKING, Optional

import yaml

from config import Config

if TYPE_CHECKING:
    from model import User

from .db import DB


class App:
    current_user: Optional["User"] = None
    db: DB

    def __init__(self, *, config_path="config.yaml"):
        self.config = self.__load_config(config_path)
        self.current_user = None

    def __load_config(self, config_path: str):
        if path.exists(config_path):
            with open(config_path, "r") as f:
                return Config(**yaml.safe_load(f))
        return Config()

    def init_db(self):
        self.db = DB(self.config.database)


app = App()

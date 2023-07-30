from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

INTRODUCTION = """WMCTF is a Jeopardy-style Online Capture The Flag Competition presented by W&M. The contest is opened to all participants around the world. Teams can compete from any location. The number of team members shall not be more than 20.The mobile phone number is an optional item, which is used to contact the prize distribution.

Platform: https://wmctf.wm-team.cn/
Registration: ssh -p 2023 wmctf.wm-team.cn
Discord: https://discord.gg/WRmvFkWnSn
QQ Group: 727697644

Enjoy your time!
"""


class Config(BaseSettings):
    database: PostgresDsn = "postgres://postgres:ctfd@db/ctfd"  # type: ignore


config = Config()

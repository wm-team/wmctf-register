from abc import ABC, abstractmethod
from typing import Any, List, Optional, TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from app.app import App


class MenuExit(Exception):
    pass


class HeadProtocol(Protocol):
    def __call__(self, /, app: "App") -> str:
        ...


class ItemBase(ABC):
    def __init__(self, name: str):
        self.name = name

    def show(self, /, app: "App") -> bool:
        return True

    @abstractmethod
    def action(self, /, app: "App") -> Optional["MenuBase"]:
        return None


class MenuBase(ABC):
    items: List[ItemBase] = []

    def head(self, /, app: "App") -> str:
        return ""

    @classmethod
    def this(cls):
        return cls()

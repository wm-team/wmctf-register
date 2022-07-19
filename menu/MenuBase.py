from abc import ABC
from typing import Callable, List, Optional, Type
from xml.sax.handler import feature_external_pes


class MenuExit(Exception):
    pass


class ItemBase(ABC):
    def __init__(self, name: str, goto: Optional[Callable[..., "MenuBase"]] = None):
        self.name = name
        self.goto = goto

    def action(self) -> bool:
        return True


class MenuBase(ABC):
    HEAD = ""
    FOOT = ""
    item: List[ItemBase] = []

    def __init__(self, item: List[ItemBase]) -> None:
        self.item = item


def run_menu(menu: MenuBase):
    current_menu = menu
    try:
        while True:
            items = current_menu.item
            exit_idx = len(items) + 1
            print("-" * 40)
            print(current_menu.HEAD)
            for idx, i in enumerate(items):
                print(f"{idx + 1}. {i.name}")
            print(f"{exit_idx}. Exit")
            print(current_menu.FOOT)
            r = input(f"[1-{exit_idx}]: ")
            try:
                if int(r) < 1 or int(r) > exit_idx:
                    continue
            except ValueError:
                continue
            if int(r) == exit_idx:
                raise MenuExit
            item = items[int(r) - 1]
            if item.action() and item.goto:
                current_menu = item.goto()
    except MenuExit:
        pass
    except KeyboardInterrupt:
        pass

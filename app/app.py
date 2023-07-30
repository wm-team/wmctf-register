from typing import Optional

import inquirer

from menu.MenuBase import MenuBase, MenuExit

from .user import User
from rich import print


class App:
    user: Optional["User"] = None

    def run_menu(self, menu: MenuBase):
        current_menu: MenuBase = menu
        try:
            while True:
                items = current_menu.items
                items = [item for item in items if item.show(app=self)]
                print("-" * 40)
                print(current_menu.head(app=self), end="")
                choices = [item.name for item in items] + ["Exit"]
                questions = [
                    inquirer.List(
                        "action",
                        message="What do you want to do?",
                        choices=choices,
                        default=choices[0],
                    )
                ]
                answers = inquirer.prompt(questions)
                if answers:
                    action = answers["action"]
                    if action == "Exit":
                        raise MenuExit()

                    item = items[choices.index(action)]
                    if ret := item.action(app=self):
                        current_menu = ret
        except MenuExit:
            pass
        except KeyboardInterrupt:
            pass

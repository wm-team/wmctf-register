from app.app import App
from app.user import User
from config import INTRODUCTION
from menu.MenuBase import MenuBase
from menu.UserMenu import UserMenu

from .MenuBase import ItemBase, MenuBase
from rich import print


class RegisterItem(ItemBase):
    def __init__(self, ):
        super().__init__("Register")

    def action(self, /, app: App):
        print("Please input your registration information:")
        user = User.register()
        if user:
            app.user = user
            return UserMenu.this()
        print("Please Try again")


class LoginItem(ItemBase):
    def __init__(self, ):
        super().__init__("Login")

    def action(self, /, app: App):
        print("Please input your login information:")
        user = User.login()
        if user:
            app.user = user
            return UserMenu.this()
        print("User not found or password is incorrect.")


class MainMenu(MenuBase):
    items = [
        RegisterItem(),
        LoginItem(),
    ]


main_menu = MainMenu()

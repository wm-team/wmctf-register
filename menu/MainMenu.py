from app import main_app
from menu.UserMenu import UserMenu
from model import User
from utils import check

from .MenuBase import ItemBase, MenuBase


class RegisterItem(ItemBase):
    def __init__(self, ):
        super().__init__("Register", UserMenu)

    def action(self) -> bool:
        print("Please input your registration information:")
        name = input("Username: ").strip()
        if not check.check_name(name):
            print("Username must be printable and between 6 and 20 characters.")
            return False
        password = input("Password: ").strip()
        if not check.check_password(password):
            print("Password must be printable and between 8 and 20 characters.")
            return False
        email = input("Email: ").strip()
        if not check.check_email(email):
            print("Email is invalid.")
            return False
        phone = input("Phone: ").strip()
        if not check.check_phone(phone) and phone != "":
            print("Phone is invalid.")
            return False
        user = User.register(main_app.db.session,
                             name=name,
                             password=password,
                             email=email,
                             phone=phone,
                             )
        if not user:
            print("User already exists.")
            return False
        main_app.current_user = user
        return True


class LoginItem(ItemBase):
    def __init__(self, ):
        super().__init__("Login", UserMenu)

    def action(self) -> bool:
        print("Please input your login information:")
        name = input("Username: ")
        password = input("Password: ")
        user = User.login(main_app.db.session,
                          name=name,
                          password=password,
                          )
        if not user:
            print("User not found or password is incorrect.")
            return False
        main_app.current_user = user
        return True


class MainMenu(MenuBase):
    HEAD = """WMCTF is a Jeopardy-style Online Capture The Flag Competition presented by W&M. The contest is opened to all participants around the world. Teams can compete from any location. The number of team members shall not be more than 20.The mobile phone number is an optional item, which is used to contact the prize distribution.

Platform: https://wmctf.wm-team.cn/
Registration: nc wmctf.wm-team.cn 2022
Discord: https://discord.gg/WRmvFkWnSn
QQ Group: 727697644

Enjoy your time!

"""

    def __init__(self):
        super().__init__([
            RegisterItem(),
            LoginItem(),
        ])


main_menu = MainMenu()

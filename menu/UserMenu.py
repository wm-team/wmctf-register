from app import main_app
from menu.MenuBase import ItemBase, MenuBase
from utils import check


class CreateTeamItem(ItemBase):
    def __init__(self):
        super().__init__("Create Team")

    def action(self) -> bool:
        user = main_app.current_user
        if not user:
            print("You are not logged in.")
            return False
        print("Please input your team information:")
        name = input("Team Name: ").strip()
        if name == "":
            print("Team name cannot be empty.")
            return False
        team = user.create_team(main_app.db.session, name=name)
        if not team:
            print("Team already exists")
        return True


class JoinTeamItem(ItemBase):
    def __init__(self):
        super().__init__("Join Team")

    def action(self) -> bool:
        user = main_app.current_user
        if not user:
            print("You are not logged in.")
            return False
        print("Please input your team information:")
        token = input("Team Token: ")
        team = user.join_team(main_app.db.session, token=token)
        if not team:
            print("Team not found")
        return True


class ExitTeamItem(ItemBase):
    def __init__(self):
        super().__init__("Exit Team")

    def action(self) -> bool:
        user = main_app.current_user
        if not user:
            print("You are not logged in.")
            return False
        user.exit_team(main_app.db.session)
        return True


class InviteItem(ItemBase):
    def __init__(self):
        super().__init__("Invite")

    def action(self) -> bool:
        user = main_app.current_user
        if not user:
            print("You are not logged in.")
            return False
        team = user.my_team(main_app.db.session)
        print("Please tell your friend to join the team with this token:")
        print(team.token)
        return True


class UserMenu(MenuBase):
    def __init__(self):
        pass

    @property
    def HEAD(self):
        user = main_app.current_user
        if not user:
            print("You are not logged in.")
            return ""
        return f"Welcome {user.name}, you are {user.team_status(main_app.db.session)}"

    @property
    def item(self):
        user = main_app.current_user
        if not user:
            print("You are not logged in.")
            return False
        if user.my_team(main_app.db.session) is None:
            return [
                CreateTeamItem(),
                JoinTeamItem(),
            ]
        else:
            return [
                InviteItem(),
                ExitTeamItem(),
            ]

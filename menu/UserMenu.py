from rich import print

from app.app import App
from app.team import Team
from menu.MenuBase import ItemBase, MenuBase
from utils import region


class ProfileItem(ItemBase):
    def __init__(self):
        super().__init__("Profile")

    def action(self, /, app: App) -> MenuBase | None:
        assert app.user, "You are not logged in."
        print("Name:", app.user.name)
        print("Email:", app.user.email)
        print("Country:", region.get_region_name((app.user.country)))
        if app.user.team:
            print("Team Name:", app.user.team.name,
                  "(Captain)" if app.user.team.captain_id == app.user.id else "")
            print("Team Members:", ', '.join(app.user.team.list_members()))


class CreateTeamItem(ItemBase):
    def __init__(self):
        super().__init__("Create Team")

    def show(self, /, app: App) -> bool:
        assert app.user, "You are not logged in."
        return bool(not app.user.team)

    def action(self, /, app: App) -> MenuBase | None:
        user = app.user
        assert user, "You are not logged in."
        print("Please input your team information:")
        team = Team.register(user.id)
        if team:
            user.join_team(team.id)
            print("Team created successfully.")
            print("Tell your teammates to join your team with the team name and password")
            return
        print("Please Try again")


class JoinTeamItem(ItemBase):
    def __init__(self):
        super().__init__("Join Team")

    def show(self, /, app: App) -> bool:
        assert app.user, "You are not logged in."
        return bool(not app.user.team)

    def action(self, /, app: App):
        user = app.user
        assert user, "You are not logged in."
        print("Please input your team information:")
        team = Team.login()
        if team:
            user.join_team(team.id)
            print("Team joined successfully.")
            return
        print("Please Try again")


class LeaveTeamItem(ItemBase):
    def __init__(self):
        super().__init__("Leave Team")

    def show(self, /, app: App) -> bool:
        user = app.user
        assert user, "You are not logged in."
        return bool(user.team)

    def action(self, /, app: App):
        user = app.user
        assert user, "You are not logged in."
        user.leave_team()


class UserMenu(MenuBase):
    def head(self, /, app: "App"):
        user = app.user
        assert user, "You are not logged in."
        return f"Welcome {user.name}\n"

    items = [
        ProfileItem(),
        CreateTeamItem(),
        JoinTeamItem(),
        LeaveTeamItem(),
    ]

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
        if not check.check_team_name(name):
            print("Team name must be printable and between 1 and 20 characters.")
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
        token = input("Team Token: ").strip()
        team = user.join_team(main_app.db.session, token=token)
        if not team:
            print("Team not found")
            return False
        elif type(team) is str:
            print(team)
            return False
        else:
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
        if not team:
            print("You are not in a team.")
            return False
        print("Please tell your friend to join the team with this token:")
        print(team.token)
        return True


class TeamInfoItem(ItemBase):
    def __init__(self):
        super().__init__("Team Info")

    def action(self) -> bool:
        user = main_app.current_user
        if not user:
            print("You are not logged in.")
            return False
        team = user.my_team(main_app.db.session)
        if not team:
            print("You are not in a team.")
            return False
        print("Team Name: " + team.name)
        print("Team Token: " + team.token)
        print("Team Members:")
        for member in user.teammates(main_app.db.session):
            print("\t" + member.name)
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
                TeamInfoItem(),
                ExitTeamItem(),
            ]

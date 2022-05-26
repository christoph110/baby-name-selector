import sys
import os
import tkinter.messagebox as msgbox
import yaml


if getattr(sys, 'frozen', False):
    basedir = os.path.dirname(sys.executable)
    appbasedir = sys._MEIPASS  # type:ignore # pylint:disable=protected-access
else:
    basedir = os.path.dirname(os.path.abspath(__file__))
    appbasedir = basedir

SETTINGS_PATH = os.path.join(basedir, "settings.yaml")
ICON_PATH = os.path.join(appbasedir, "peanut.ico")
RESULTS_DIR = os.path.join(basedir, "results")
NAMEFILES_DIR = os.path.join(basedir, "name_lists")


class UserSettings:
    # user settings
    user1: dict
    user2: dict
    two_users: bool
    results_file: str

    @classmethod
    def load(cls) -> None:
        try:
            with open(SETTINGS_PATH, "r", encoding="utf8") as file:
                try:
                    settings_dict = yaml.safe_load(file)
                    cls.settings_parser(settings_dict)
                except yaml.YAMLError as err:
                    cls.error_msg(
                        msg=(f"Error while loading settings{err.args[1]}\n"
                             + err.args[2]))
                    raise yaml.YAMLError from err

        except FileNotFoundError as err:
            cls.error_msg(msg=(f"Error while trying to load {SETTINGS_PATH}\n"
                               + err.args[1]))
            raise FileNotFoundError from err

    @classmethod
    def settings_parser(cls, settings_dict: dict) -> None:
        cls.user1 = settings_dict["user_1"]
        cls.user2 = settings_dict["user_2"]
        cls.two_users = bool(cls.user2["name"])
        cls.results_file = os.path.join(RESULTS_DIR,
                                        settings_dict["results_file"])

    @staticmethod
    def error_msg(msg: str) -> None:
        msgbox.showerror(title='ERROR',
                         message=msg)

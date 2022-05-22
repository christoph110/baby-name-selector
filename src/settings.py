import sys
import os
import yaml
from interface import NameSelector
import tkinter.messagebox as msgbox


if getattr(sys, 'frozen', False):
    basedir = os.path.dirname(sys.executable)
else:
    basedir = os.path.dirname(os.path.abspath(__file__))

SETTINGS_PATH = os.path.join(basedir, "settings.yaml")


with open(SETTINGS_PATH, "r") as file:
    try:
        settings = yaml.safe_load(file)
    except yaml.YAMLError as err:
        msgbox.showinfo(title='ERROR', message=err)


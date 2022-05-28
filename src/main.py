"""
Main module
To be started directly via 'python main.py'
"""
from settings import UserSettings
from functions import (initialize_files,
                       get_new_name_list,
                       randomize_list)
from interface import NameSelector


name_selector = NameSelector()
UserSettings.load()
initialize_files()
new_names_list = get_new_name_list()
randomize_list(new_names_list)
name_selector.set_frames()
name_selector.run(name_list=new_names_list)

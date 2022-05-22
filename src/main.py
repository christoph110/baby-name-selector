from settings import UserSettings
from functions import (initialize_results_file,
                       get_new_name_list,
                       randomize_list)
from interface import NameSelector


name_selector = NameSelector()
UserSettings.load()
initialize_results_file()
new_names_list = get_new_name_list()
randomize_list(new_names_list)
name_selector.set_frames()
name_selector.run(name_list=new_names_list)

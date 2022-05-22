import os
import sys
import settings
from functions import get_new_name_list, randomize_list
from interface import NameSelector

if getattr(sys, 'frozen', False):
    basedir = os.path.dirname(sys.executable)
else:
    basedir = os.path.dirname(os.path.abspath(__file__))

NAMEFILES_DIR = os.path.join(basedir, "name_lists")
DB_FILE = os.path.join(basedir, "database", "db.csv")

new_names_list = get_new_name_list(db_file=DB_FILE,
                                   namefiles_dir=NAMEFILES_DIR)
randomize_list(new_names_list)
name_selector = NameSelector(name_list=new_names_list, db_file=DB_FILE)

"""module with backend functionalities"""
import os
import sys
import random
import tkinter.messagebox as msgbox
import pandas as pd
from pandas.errors import ParserError
import settings
from settings import UserSettings
from utils import error_message


def load_db() -> dict:
    """loads the file where the selection results are stored"""
    result = pd.DataFrame(pd.read_csv(UserSettings.results_file, sep=";"))
    result_dict = {}
    for row in result.itertuples():
        key = f"{row.name};{row.sex}"
        result_dict[key] = {
            "user1_response": getattr(row, UserSettings.user1["name"]),
        }
        if UserSettings.two_users:
            result_dict[key]["user2_response"] = getattr(
                row, UserSettings.user2["name"])
    return result_dict


def load_names() -> pd.DataFrame:
    """loads all names from all files in the names-files directory"""
    dirname = settings.NAMEFILES_DIR
    names_df = pd.DataFrame()
    for filename in os.listdir(dirname):
        filepath = os.path.join(dirname, filename)
        file_df = file_to_df(filepath)
        names_df = pd.concat([names_df, file_df])
        names_df = names_df.reset_index(drop=True)
        # formatting
        names_df["sex"] = names_df["sex"].str.lower()
        names_df["name"] = names_df["name"].str.capitalize()
        names_df["name"] = names_df["name"].str.strip()
    return names_df


def file_to_df(filepath: str) -> pd.DataFrame:
    """
    loads a file with a list of sex;name and returns a dataframe
    after validating the file for the correct format
    """
    try:
        file_df = pd.DataFrame(pd.read_csv(filepath, sep=";",
                                           names=['sex', 'name'],
                                           dtype=str,
                                           keep_default_na=False))
    except (ParserError, PermissionError) as err:
        error_message(title="ParserError",
                      msg=err.args[0] + f" in {filepath}")
    # validation
    empty_rows = file_df[
        file_df.applymap(lambda x: x.strip() == "").any(axis=1)].index.values
    if len(empty_rows) > 0:
        error_message(
            title="Corrupt names list file",
            msg=f"empty values in rows {empty_rows + 1} in {filepath}")
    if not set(file_df.sex.unique()).issubset({"f", "m"}):
        error_message(
            title="Corrupt names list file",
            msg=f"'sex' has to be either 'm' or 'f' "
                f"but was {set(file_df.sex.unique())} in {filepath}")
    return file_df


def get_new_name_list() -> list[str]:
    """
    returns a list of names (sex;name) that are not
    present in the results yet
    """
    results: dict = load_db()
    names: pd.DataFrame = load_names()
    new_names_list = []
    for row in names.itertuples():
        key = f"{row.name};{row.sex}"
        if key not in results:
            new_names_list.append(key)
    return new_names_list


def randomize_list(my_list: list) -> None:
    """shuffles a list (inplace)"""
    seed = 0
    random.seed(seed)
    random.shuffle(my_list)


def add_result_to_db(name_item: dict) -> None:
    """add a new result row to the results file"""
    with open(UserSettings.results_file, "a", encoding="utf8") as file:
        data = ";".join([
            name_item['name'],
            name_item['sex'],
            name_item['user1_response']
        ])
        if UserSettings.two_users:
            data += f";{name_item['user2_response']}"
        data += "\n"
        file.write(data)


def initialize_files() -> None:
    """creates files/folders and validates present files"""
    create_dirs()
    results_path = UserSettings.results_file
    # Create file if it does not exist
    if not os.path.isfile(results_path):
        create_results_file()
    # appends newline at the end of the file if not existant
    with open(results_path, "r+", encoding="utf8") as file:
        data = file.read()
        if data[-1] != "\n":
            file.write("\n")
    # validate file
    try:
        results_df = pd.DataFrame(pd.read_csv(results_path,
                                              sep=";",
                                              header=0,
                                              dtype=str,
                                              keep_default_na=False))
    except (ParserError, PermissionError) as err:
        error_message(title="ParserError",
                      msg=err.args[0] + f" in {results_path}")
    validate_results_file(results_df)


def create_dirs():
    """creates necessary dictionaries"""
    if not os.path.isdir(settings.RESULTS_DIR):
        os.mkdir(settings.RESULTS_DIR)
    if not os.path.isdir(settings.NAMEFILES_DIR):
        os.mkdir(settings.NAMEFILES_DIR)
        msg = ("It seems that you are running the Name Selector for "
               "the first time. To get started, just drop some files "
               "with names into the following folder:\n\n"
               f"{settings.NAMEFILES_DIR}\n\n"
               "(Look into the catalog folder for some examples)\n"
               "Restart the application and you are ready to go.\n\n"
               "Have fun! :)")
        msgbox.showinfo(title="Welcome",
                        message=msg)
        sys.exit()


def validate_results_file(results_df: pd.DataFrame) -> None:
    """validates the results file for the correct format"""
    results_path = UserSettings.results_file
    file_columns = results_df.columns
    result_columns = ["name", "sex", UserSettings.user1["name"]]
    if UserSettings.two_users:
        result_columns.append(UserSettings.user2["name"])
    if set(file_columns) != set(result_columns):
        error_message(
            title="Corrupt results file",
            msg=f"Incorrect column names in {results_path}\n"
                f"Was expecting {result_columns} but was "
                f"{file_columns}\n\n"
                f"Did you select the wrong results file in 'settings.yaml'?")

    empty_rows = results_df[
        results_df.applymap(lambda x: x.strip() == "").any(axis=1)
    ].index.values
    if len(empty_rows) > 0:
        error_message(
            title="Corrupt results file",
            msg=f"empty values in rows {empty_rows + 2} in {results_path}")
    if not set(results_df.sex.unique()).issubset({"f", "m"}):
        error_message(
            title="Corrupt results file",
            msg=f"'sex' has to be either 'm' or 'f' "
                f"but was {set(results_df.sex.unique())} in {results_path}")


def create_results_file() -> None:
    """creates a new results file"""
    with open(UserSettings.results_file, "w", encoding="utf8") as file:
        file.write(";".join(["name", "sex", UserSettings.user1['name']]))
        if UserSettings.two_users:
            file.write(f";{UserSettings.user2['name']}")
        file.write("\n")

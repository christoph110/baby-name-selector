import os
import random
import tkinter.messagebox as msgbox
import pandas as pd
from pandas.errors import ParserError
from settings import UserSettings


def load_db() -> dict:
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
    dirname = UserSettings.namefiles_dir
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
    try:
        file_df = pd.DataFrame(pd.read_csv(filepath, sep=";",
                                           names=['sex', 'name'],
                                           dtype=str,
                                           keep_default_na=False))
    except ParserError as err:
        raise ParserError(err.args[0] + f" in {filepath}") from err
    # validation
    empty_rows = file_df[
        file_df.applymap(lambda x: x.strip() == "").any(axis=1)].index.values
    if len(empty_rows) > 0:
        raise_validation_error(
            title="Corrupt names list file",
            msg=f"empty values in rows {empty_rows + 1} in {filepath}")
    if not set(file_df.sex.unique()).issubset({"f", "m"}):
        raise_validation_error(
            title="Corrupt names list file",
            msg=f"'sex' has to be either 'm' or 'f' "
                f"but was {set(file_df.sex.unique())} in {filepath}")
    return file_df


def get_new_name_list() -> list[str]:
    results: dict = load_db()
    names: pd.DataFrame = load_names()
    new_names_list = []
    for row in names.itertuples():
        key = f"{row.name};{row.sex}"
        if key not in results:
            new_names_list.append(key)
    return new_names_list


def randomize_list(my_list: list) -> None:
    seed = 0
    random.seed(seed)
    random.shuffle(my_list)


def add_result_to_db(name_item: dict) -> None:
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


def initialize_results_file() -> None:
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
    except ParserError as err:
        raise ParserError(err.args[0] + f" in {results_path}") from err
    validate_results_file(results_df)


def validate_results_file(results_df: pd.DataFrame) -> None:
    results_path = UserSettings.results_file
    file_columns = results_df.columns
    result_columns = ["name", "sex", UserSettings.user1["name"]]
    if UserSettings.two_users:
        result_columns.append(UserSettings.user2["name"])
    if set(file_columns) != set(result_columns):
        raise_validation_error(
            title="Corrupt results file",
            msg=f"Incorrect column names in {results_path}\n"
                f"Was expecting {result_columns} but was "
                f"{file_columns}\n\n"
                f"Did you select the wrong results file in 'settings.yaml'?")

    empty_rows = results_df[
        results_df.applymap(lambda x: x.strip() == "").any(axis=1)
    ].index.values
    if len(empty_rows) > 0:
        raise_validation_error(
            title="Corrupt results file",
            msg=f"empty values in rows {empty_rows + 2} in {results_path}")
    if not set(results_df.sex.unique()).issubset({"f", "m"}):
        raise_validation_error(
            title="Corrupt results file",
            msg=f"'sex' has to be either 'm' or 'f' "
                f"but was {set(results_df.sex.unique())} in {results_path}")


def raise_validation_error(title: str, msg: str) -> None:
    msgbox.showerror(title=title,
                     message=msg)
    raise AssertionError(msg)


def create_results_file() -> None:
    with open(UserSettings.results_file, "w", encoding="utf8") as file:
        file.write(";".join(["name", "sex", UserSettings.user1['name']]))
        if UserSettings.two_users:
            file.write(f";{UserSettings.user2['name']}")
        file.write("\n")

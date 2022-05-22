import os
import random
import pandas as pd
from pandas.errors import ParserError


def load_db(result_file: str) -> dict:
    result = pd.DataFrame(pd.read_csv(result_file, sep=";"))
    result_dict = {}
    for row in result.itertuples():
        key = f"{row.name};{row.sex}"
        result_dict[key] = {
            "user1_response": row.user1_response,
            "user2_response": row.user2_response,
        }
    return result_dict


def load_names(namefiles_dir: str) -> pd.DataFrame:
    names_df = pd.DataFrame()
    for filename in os.listdir(namefiles_dir):
        filepath = os.path.join(namefiles_dir, filename)
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
    if empty_rows:
        raise AssertionError(
            f"empty values in rows {empty_rows} in {filepath}")
    if not set(file_df.sex.unique()).issubset({"f", "m"}):
        raise AssertionError(
            f"'sex' has to be either 'm' or 'f' "
            f"but was {set(file_df.sex.unique())} in {filepath}")
    return file_df


def get_new_name_list(db_file: str, namefiles_dir: str) -> list[str]:
    results: dict = load_db(db_file)
    names: pd.DataFrame = load_names(namefiles_dir)
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


def add_result_to_db(db_file: str, name_item: dict) -> None:
    with open(db_file, "a", encoding="utf8") as file:
        data = ";".join([
            name_item['name'],
            name_item['sex'],
            name_item['user1_response'],
            name_item['user2_response']
        ])
        file.write(data)

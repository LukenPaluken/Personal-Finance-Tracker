import os
import json
from tabulate import tabulate
import constants as con


def clean_screen() -> None:
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


def print_logo() -> None:
    pantalla = [["Personal Finance Tracker by Lucas Paluci"], [con.ART_TEXT]]
    print(tabulate(pantalla, colalign=("center",)))


def show_options(options: list[str]) -> None:
    """ """
    for num, option in enumerate(options, start=1):
        print(f"{num}. {option}")
    print()


def read_json(file_dir: str) -> dict:
    """ """
    try:
        with open(file_dir, "rt", encoding="utf-8") as f:
            dictionary = json.load(f)
    except FileNotFoundError:
        dictionary = {}
    return dictionary


def write_json(file_dir: str, dictionary: dict) -> bool:
    """ """
    if not os.path.isdir("data"):
        os.mkdir("data")
    try:
        with open(file_dir, "wt", encoding="utf-8") as f:
            myjson = json.dumps(dictionary)
            f.write(myjson)
    except FileNotFoundError:
        return False
    return True

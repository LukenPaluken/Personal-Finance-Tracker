import os
import json
from tabulate import tabulate
import constants as con


def clean_screen() -> None:
    """
    Clears screen depending on operating system.
    """
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


def print_logo() -> None:
    """
    Prints logo and formats it with Tabulate.
    """
    screen = [["Personal Finance Tracker by Lucas Paluci"], [con.ART_TEXT]]
    print(tabulate(screen, colalign=("center",)))


def show_options(options: list[str]) -> None:
    """
    Prints a list of options.
    
    Parameters:
        options: list[str]
    """
    for num, op in enumerate(options, start=1):
        print(f"{num}. {op}")
    print()


def read_json(file_path: str) -> dict:
    """
    Reads a JSON in specified path and returns it as a dictionary.
    
    If file isn't found, it returns an empty dictionary.
    
    Parameters:
        file_path: str.
    
    Returns: 
        dictionary: dict.
    """
    try:
        with open(file_path, 'rt', encoding='utf-8') as f:
            dictionary = json.load(f)
    except FileNotFoundError:
        dictionary = {}
    return dictionary


def write_json(file_path: str, dictionary: dict) -> bool:
    """
    Creates 'data' directory if it doesn't exist.
    
    Opens file in specified path and dumps dictionary.
    
    Parameters:
        file_path: str.
        dictionary: dict.
        
    Returns:
        bool
    """
    if not os.path.isdir('data'):
        os.mkdir('data')
    try:
        with open(file_path, 'wt', encoding='utf-8') as f:
            myjson = json.dumps(dictionary)
            f.write(myjson)
    except FileNotFoundError:
        return False
    return True

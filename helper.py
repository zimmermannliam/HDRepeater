"""
Helper functions for hdrepeater.py
"""

import json
import pathlib
import os
import subprocess

def dict_merge(first: dict, second: dict) -> dict:
    """ Return merged list with first and second, prioritizing first 
        but letting Nones drop through. Does not modify first or
        second. """
    ret = first.copy()
    for key,second_val in second.items():
        if ret.get(key, None) is None:
            ret[key] = second_val
    return ret


def print_v(msg: str, verbose: bool) -> None:
    """ Print msg only if verbose is True """
    if verbose:
        print(msg)


def load_json(json_path: pathlib.Path) -> dict:
    """ Get a json from json_path, or else return None """
    if not json_path.is_file():
        return None
    with open(json_path, 'r') as json_file:
        return json.load(json_file)


def cp(src: str, dest: str) -> None:
    """ Copy a file from src to dest using the correct copy command for the OS """
    if os.name == "nt":
        subprocess.run(["copy", src, dest])
    subprocess.run(["cp", src, dest])

import os


def split_name_ext(path: str) -> (str, str):
    return os.path.splitext(path)
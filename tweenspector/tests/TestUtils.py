from pathlib import Path
import sys


def add_parent_dir_to_sys_path():
    path = str(Path().absolute().parent)
    if path not in sys.path:
        sys.path.append(path)

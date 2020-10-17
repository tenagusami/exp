#! /usr/bin/python3
"""

"""
import os
from subprocess import call
import re
import pathlib as p
import sys
from functools import reduce
from typing import List


class Error(Exception):
    """
    The fundamental exception class
    """
    pass


class NotInspectableError(Error):
    """
    The Error when the path on a pure WSL2 filesystem is inspected.
    """
    pass


class UsageError(Error):
    """
    The error for usage of a function.
    """
    pass


def wsl2_full_path2windows_path(wsl2_path: p.Path) -> p.PureWindowsPath:
    """
    convert a wsl2 path (posix path) to the corresponding windows path.
    Args:
        wsl2_path(pathlib.Path):  wsl2 path

    Returns:
        windows path(pathlib.Path)
    Raises:
        UsageError: wsl2_path is not correct WSL2 path.
    """
    try:
        [(drive, path)] = re.findall(r"^/mnt/([a-z])(/?.*)", wsl2_path.as_posix())
    except ValueError:
        raise UsageError(f"The input path must be a correct WSL2 path (function {__name__}).")
    return reduce(lambda reduced, name: reduced.joinpath(name), p.Path(path).parts,
                  p.PureWindowsPath(rf"{drive}:\\"))


def is_wsl2_path(path: p.PurePath) -> bool:
    """
    Whether the given path is a correct WSL2 path.
    Args:
        path(pathlib.Path): a path

    Returns:
        True if correct.
    """
    return re.match(r"^/mnt/[a-z]/", path.as_posix()) is not None


def get_path(arguments: List[str]) -> p.Path:
    """
    Convert the WSL2 path specified as the command line argument to a pathlib.Path object.
    If nothing is specified, the current directory is used.
    Args:
        arguments(List[str]): the command line argument

    Returns:
        path object(pathlib.Path)
    """
    if len(arguments) == 2:
        return p.Path(sys.argv[1]).resolve()
    elif len(arguments) == 1:
        return p.Path(".").resolve()
    raise UsageError(f"# of command line arguments must be 1 (function {__name__}).")


def open_on_windows(explorer: p.Path, path: p.Path) -> None:
    """

    Args:
        explorer(pathlib.Path): the path to the windows explorer.
        path(pathlib.Path): the specified path.

    Raises:
        NotInspectableError: the specified path is not inspectable from Windows system.
    """
    if is_wsl2_path(path):
        windows_path = wsl2_full_path2windows_path(path)
        call([explorer, windows_path])
        return
    raise NotInspectableError(f"The specified path {p.Path} is not in the windows filesystem "
                              + f"(function {__name__}).")


def main() -> None:
    """
    The main procedure
    """
    if os.name == "nt":
        print(f"This tool {__file__} is usable only on WSL2.")
        sys.exit(1)
    try:
        explorer: p.Path = p.Path(r"/mnt") / "c" / "Windows" / "explorer.exe"
        path: p.Path = get_path(sys.argv)
        open_on_windows(explorer, path)
    except(UsageError, NotInspectableError) as e:
        sys.stderr.write(e.args[0])
        sys.exit(1)


if __name__ == '__main__':
    main()
    sys.exit(0)

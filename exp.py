#! /usr/bin/python3
import subprocess as s
import os as o
import re
import sys


def WSL_full_path2windows_path(wsl_path):
    [(drive, path)] = re.findall(r"^/mnt/([a-z])(.*)", wsl_path)
    return drive+":"+path.replace("/", "\\")


def is_WSL_path(path):
    return re.match(r"^/mnt/[a-z]\/", path)


if __name__ == '__main__':
    explorer = "/mnt/c/Windows/explorer.exe"
    file_path = "."
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    file_absolute_path = o.path.realpath(o.path.abspath(file_path))
    if is_WSL_path(file_absolute_path):
        windows_path = WSL_full_path2windows_path(file_absolute_path)
        s.call([explorer, windows_path])
    else:
        sys.stderr.write("The specified path is not in the windows filesystem")






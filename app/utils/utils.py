import sys


def get_os():
    os_name = sys.platform
    if os_name == "win32" or os_name == "cygwin":
        return "Windows"
    else:
        return "MacOS"


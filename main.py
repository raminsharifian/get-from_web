import os
from access.os_access import os_access
from sys import argv
from utils.curl import curl

URL = "http://localhost:3000"


def main():
    curl(URL, "./caches")
    print("os: {}".format(os.name))


if __name__ == "__main__":
    os_access(os.name, main)

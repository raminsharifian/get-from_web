import os
from access.os_access import os_access
from sys import argv

URL = "http://localhost:3000"


def main():
    os.system(f"mkdir -p ./{argv[1]}")
    os.system(f"curl -s {URL} | grep -oP '(?<=href=\")[^\"]*' > ./{argv[1]}/urls.txt")

    print("os: {}".format(os.name))


if __name__ == "__main__":
    os_access(os.name, main)

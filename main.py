import os
from access.os_access import os_access


def main():
    print("os: {}".format(os.name))


if __name__ == "__main__":
    os_access(os.name, main)

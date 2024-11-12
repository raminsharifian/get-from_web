from os import system


def curl(url, path_to_save="."):
    system(f"mkdir -p {path_to_save}")
    system(f"curl -s {url} | grep -oP '(?<=href=\")[^\"]*' > {path_to_save}/urls.txt")

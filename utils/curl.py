import os
import subprocess
import logging
from urllib.parse import urlparse


def curl(url: str, path_to_save: str = "."):
    """
    Fetches URLs from a webpage and saves them to a text file.

    This function uses `curl` to fetch the HTML content of the provided URL,
    extracts all the hyperlinks (href attributes), and saves them into a file
    named `urls.txt` within the specified directory.

    Parameters:
        url (str): The URL of the webpage to scrape links from.
        path_to_save (str): Directory where the extracted URLs will be saved.
                             Defaults to the current directory.

    Raises:
        ValueError: If the URL is invalid or not reachable.
        FileNotFoundError: If the specified directory for saving the file does not exist.
    """

    # Ensure the provided directory exists
    try:
        os.makedirs(path_to_save, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create directory {path_to_save}: {e}")
        raise FileNotFoundError(f"Unable to create directory {path_to_save}")

    # Validate the URL format
    if not urlparse(url).scheme:
        raise ValueError(
            f"Invalid URL: {url}. Please provide a valid URL including the scheme (e.g., http://)."
        )

    # Construct the command to fetch the HTML content and extract href links
    try:
        curl_command = ["curl", "-s", url]
        grep_command = ["grep", "-oP", '(?<=href=")[^"]*']

        # Run the curl command to fetch the HTML content and get output as string (not bytes)
        result = subprocess.run(
            curl_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        # No need to decode stdout, as it's already a string
        decoded_output = result.stdout

        # Process the output with grep
        grep_result = subprocess.run(
            grep_command,
            input=decoded_output,
            text=True,
            capture_output=True,
            check=True,
        )

        # Save the extracted URLs to the file
        with open(os.path.join(path_to_save, "urls.txt"), "w") as file:
            file.write(grep_result.stdout)

        logging.info(f"URLs successfully saved to {path_to_save}/urls.txt")

    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while executing command: {e}")
        raise RuntimeError(
            f"Failed to fetch or parse content from {url}. Check the URL or your network connection."
        )

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise

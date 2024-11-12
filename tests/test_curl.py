import unittest
from unittest.mock import patch, MagicMock
import os
import subprocess
import logging
from io import StringIO
from utils.curl import curl


class TestCurlFunction(unittest.TestCase):
    @patch("subprocess.run")  # Mock subprocess.run to avoid calling actual curl/grep
    @patch("os.makedirs")  # Mock os.makedirs to prevent actual directory creation
    def test_curl(self, mock_makedirs, mock_subprocess_run):
        # Mocking subprocess.run for curl and grep commands
        mock_curl_result = MagicMock()
        mock_curl_result.stdout = b'<html><a href="http://example.com">Example</a></html>'  # Simulated curl output
        mock_curl_result.stderr = b""
        mock_subprocess_run.return_value = mock_curl_result

        # Simulating the grep command's output (extracted URLs)
        mock_grep_result = MagicMock()
        mock_grep_result.stdout = "http://example.com\n"
        mock_subprocess_run.return_value = mock_grep_result

        # Create a temporary directory to ensure the path exists
        temp_dir = "./mocked_path"
        os.makedirs(temp_dir, exist_ok=True)  # Ensure the directory exists

        # Create a capture for logging output
        log_stream = StringIO()
        logging.basicConfig(stream=log_stream, level=logging.INFO)

        # Call the function to test
        curl("http://fakeurl.com", temp_dir)

        # Check that os.makedirs was called to create the directory
        mock_makedirs.assert_called_once_with(temp_dir, exist_ok=True)

        # Check that subprocess.run was called for curl and grep
        mock_subprocess_run.assert_any_call(
            ["curl", "-s", "http://fakeurl.com"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        mock_subprocess_run.assert_any_call(
            ["grep", "-oP", '(?<=href=")[^"]*'],
            input="http://example.com\n",
            text=True,
            capture_output=True,
            check=True,
        )

        # Check the logging output to confirm success message
        self.assertIn(
            "URLs successfully saved to ./mocked_path/urls.txt", log_stream.getvalue()
        )

        # Verify that the output file would be written with the correct content
        with open(os.path.join(temp_dir, "urls.txt"), "r") as file:
            content = file.read()
            self.assertEqual(content, "http://example.com\n")


if __name__ == "__main__":
    unittest.main()

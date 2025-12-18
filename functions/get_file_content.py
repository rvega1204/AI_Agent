"""
File Content Reading Tool

This module provides functionality to read file contents within a sandboxed
working directory. It's used by the AI agent to examine source code,
configuration files, and other text files.
"""

import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    """
    Read and return the contents of a file.

    This function reads a file within the working directory sandbox and returns
    its contents as a string. Files larger than MAX_CHARS are truncated with a
    notice appended.

    Args:
        working_directory (str): The base directory that acts as the sandbox root
        file_path (str): Path to the file to read, relative to working_directory

    Returns:
        str: The file contents (up to MAX_CHARS characters) or an error message

    Security:
        - Validates that the file path is within working_directory
        - Prevents path traversal attacks using absolute path comparison
        - Only reads regular files (not directories or special files)

    Limits:
        - Maximum characters read: 10,000
        - Files exceeding this limit are truncated with a notice

    Example:
        >>> get_file_content("/home/user/project", "main.py")
        'import os\\nimport sys\\n...'
    """
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file_content_string = ""
        with open(abs_file_path, "r") as f:
            file_content_string += f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_string
    except Exception as e:
        return f'Error: {str(e)}'
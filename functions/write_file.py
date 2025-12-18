"""
File Writing Tool

This module provides functionality to write files within a sandboxed working
directory. It's used by the AI agent to create or modify files as part of
completing tasks.
"""

import os

def write_file(working_directory, file_path, content):
    """
    Write content to a file, creating it if it doesn't exist.

    This function writes content to a file within the working directory sandbox.
    It automatically creates parent directories if they don't exist. The file
    will be overwritten if it already exists.

    Args:
        working_directory (str): The base directory that acts as the sandbox root
        file_path (str): Path to the file to write, relative to working_directory
        content (str): The content to write to the file

    Returns:
        str: Success message with character count or error message

    Security:
        - Validates that the file path is within working_directory
        - Prevents path traversal attacks using absolute path comparison
        - Prevents writing to directories (only regular files)
        - Creates parent directories safely with os.makedirs

    Example:
        >>> write_file("/home/user/project", "output.txt", "Hello, World!")
        'Successfully wrote to "output.txt" (13 characters written)'
    """
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = os.path.dirname(abs_file_path)
        os.makedirs(parent_dir, exist_ok=True)

        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"
    
    
    



"""
File Information Listing Tool

This module provides functionality to list files and directories within a
sandboxed working directory. It's used by the AI agent to explore the
filesystem structure.
"""

import os


def get_files_info(working_directory, directory="."):
    """
    List files and directories with their metadata.

    This function lists the contents of a directory, providing file size and
    directory status for each item. It enforces security by ensuring that only
    paths within the working directory can be accessed.

    Args:
        working_directory (str): The base directory that acts as the sandbox root
        directory (str, optional): The subdirectory to list, relative to working_directory.
                                  Defaults to "." (current directory)

    Returns:
        str: A formatted string listing each file/directory with:
             - Name
             - Size in bytes
             - Whether it's a directory (True/False)
             Or an error message if the operation fails

    Security:
        - Validates that the target directory is within working_directory
        - Uses os.path.commonpath to prevent directory traversal attacks
        - Returns error if attempting to access outside the sandbox

    Example:
        >>> get_files_info("/home/user/project", ".")
        '- main.py: file_size=1234 bytes, is_dir=False\\n- tests: file_size=4096 bytes, is_dir=True\\n'
    """
    try:
        # Get absolute path of working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Construct and normalize the target directory path
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Validate that target directory is within working directory
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if target is actually a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # List contents of the directory
        response = ""
        contents = os.listdir(target_dir)
        for content in contents:
            content_path = os.path.join(target_dir, content)
            is_dir = os.path.isdir(content_path)
            size = os.path.getsize(content_path)
            response += f"- {content}: file_size={size} bytes, is_dir={is_dir}\n"

        return response

    except Exception as e:
        return f"Error: {str(e)}"
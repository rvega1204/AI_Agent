"""
Python File Execution Tool

This module provides functionality to execute Python files within a sandboxed
working directory. It's used by the AI agent to run scripts, tests, and other
Python programs.
"""

import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    """
    Execute a Python file and capture its output.

    This function runs a Python script within the working directory sandbox and
    captures both stdout and stderr. It has a 30-second timeout to prevent
    infinite loops.

    Args:
        working_directory (str): The base directory that acts as the sandbox root
        file_path (str): Path to the Python file to execute, relative to working_directory
        args (list, optional): Command-line arguments to pass to the script

    Returns:
        str: The output from the script (stdout and/or stderr) or an error message.
             Format includes:
             - "Process exited with code X" if non-zero exit
             - "No output produced" if empty output
             - "STDOUT: ..." for standard output
             - "STDERR: ..." for standard error

    Security:
        - Validates that the file path is within working_directory
        - Prevents path traversal attacks using absolute path comparison
        - Only executes .py files
        - 30-second timeout prevents runaway processes
        - Executes in the working directory context

    Example:
        >>> run_python_file("/home/user/project", "tests.py")
        'STDERR:\\n.........\\n----------------------------------------------------------------------\\nRan 9 tests in 0.001s\\n\\nOK\\n'
    """
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_file_path.startswith(abs_working_dir + os.sep):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_file_path]

        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True,
            text=True
        )

        output_parts = []

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
            

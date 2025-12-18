"""
Function Schemas for LLM Tool Calling

This module defines the function schemas (tool definitions) that are provided
to the LLM to enable function calling capabilities. These schemas follow the
OpenAI/Groq function calling format.

Each schema includes:
- Function name
- Description of what the function does
- Parameters (with types and descriptions)
- Required parameters

The LLM uses these schemas to understand what tools are available and how to
call them correctly. The actual function implementations are in the functions/
directory.

Security Note:
    All functions are sandboxed to operate within a specified working directory.
    The LLM cannot access files or directories outside this sandbox.
"""

# Function schemas for LLM function calling using Groq/OpenAI format

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (use '.' for current directory)"
                }
            }
        }
    }
}

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads and returns the content of a specified file (up to 10,000 characters)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                }
            },
            "required": ["file_path"]
        }
    }
}

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a file at the specified path, creating directories if needed",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                }
            },
            "required": ["file_path", "content"]
        }
    }
}

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file and returns its output (stdout and stderr)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional command-line arguments to pass to the Python script",
                }
            },
            "required": ["file_path"]
        }
    }
}

# List of all available functions
available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
]

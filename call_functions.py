from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
import json

working_directory = 'calculator'

def call_function(function_call, verbose=False):
    """
    Calls one of the available functions based on the function_call object.

    Args:
        function_call: An object with .name and .arguments properties
                      (e.g., tool_call.function from Groq API)
        verbose: If True, prints detailed function call information

    Returns:
        A dictionary with the result or error
    """
    # Parse arguments if they're a JSON string
    if isinstance(function_call.arguments, str):
        args = json.loads(function_call.arguments)
    else:
        args = function_call.arguments

    function_name = function_call.name

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    # Map function names to actual functions
    function_map = {
        'get_files_info': get_files_info,
        'get_file_content': get_file_content,
        'write_file': write_file,
        'run_python_file': run_python_file
    }

    # Check if function exists
    if function_name not in function_map:
        error_response = {
            "role": "tool",
            "tool_call_id": getattr(function_call, 'id', None),
            "name": function_name,
            "content": json.dumps({"error": f"Unknown function: {function_name}"})
        }
        return error_response

    # Add working_directory to args
    args['working_directory'] = working_directory

    # Call the function
    try:
        result = function_map[function_name](**args)

        # Create response
        response = {
            "role": "tool",
            "tool_call_id": getattr(function_call, 'id', None),
            "name": function_name,
            "content": json.dumps({"result": result})
        }

        if verbose:
            print(f"-> {json.loads(response['content'])}")

        return response

    except Exception as e:
        error_response = {
            "role": "tool",
            "tool_call_id": getattr(function_call, 'id', None),
            "name": function_name,
            "content": json.dumps({"error": str(e)})
        }

        if verbose:
            print(f"-> Error: {str(e)}")

        return error_response

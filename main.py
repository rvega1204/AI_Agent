"""
AI Agent with Function Calling - Main Entry Point

This module implements an agentic AI system that can autonomously use tools
to accomplish complex tasks. It uses the Groq API with function calling
capabilities to interact with the filesystem in a sandboxed environment.

The agent can:
- List files and directories
- Read file contents
- Write files
- Execute Python scripts

The agent uses an iterative approach, making up to 20 API calls to complete
a task, allowing it to gather information, process it, and take actions based
on the results.

Usage:
    python main.py "your prompt here" [--verbose]

Example:
    python main.py "Find and fix bugs in the tests.py file"
    python main.py "List all Python files and explain what they do" --verbose
"""

import os
import argparse
import sys
import time
import json
from dotenv import load_dotenv
from groq import Groq, RateLimitError
from functions.get_files_info import get_files_info
from call_function import (
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file
)
from call_functions import call_function


def call_groq_with_retry(client, model, messages, tools=None, max_retries=2, suppress_tool_errors=False):
    """
    Call Groq API with retry logic to handle rate limits.

    This function wraps the Groq API call with retry logic to handle rate limit
    errors gracefully. If a rate limit is hit, it waits 30 seconds before retrying.

    Args:
        client (Groq): The Groq API client instance
        model (str): The model ID to use (e.g., 'llama-3.3-70b-versatile')
        messages (list): List of message dictionaries in the conversation
        tools (list, optional): List of function schemas available to the model
        max_retries (int): Maximum number of retry attempts (default: 2)
        suppress_tool_errors (bool): Whether to suppress tool_use_failed errors (default: False)

    Returns:
        ChatCompletion: The API response object

    Raises:
        RateLimitError: If max retries are exceeded
        Exception: For other API errors
    """
    for attempt in range(max_retries):
        try:
            kwargs = {
                "model": model,
                "messages": messages
            }
            if tools:
                kwargs["tools"] = tools

            response = client.chat.completions.create(**kwargs)
            return response
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 30
                print(f"Rate limit reached. Waiting {wait_time} seconds...")
                sys.stdout.flush()
                time.sleep(wait_time)
                print("Retrying...")
                sys.stdout.flush()
            else:
                print("Max retries reached. Try again later.")
                raise
        except Exception as e:
            # Suppress tool_use_failed errors if requested (for fallback handling)
            if not (suppress_tool_errors and 'tool_use_failed' in str(e)):
                print(f"Error: {e}")
            raise


def main():
    """
    Main entry point for the AI Agent.

    This function:
    1. Loads environment variables and API credentials
    2. Parses command-line arguments
    3. Sets up the conversation with system prompt and user message
    4. Runs the agentic loop (up to 20 iterations) where the model can:
       - Call tools to gather information
       - Process results
       - Take actions based on findings
       - Provide final response
    5. Handles errors and edge cases gracefully

    The agentic loop continues until:
    - The model provides a final text response without tool calls
    - An error occurs
    - Maximum iterations (20) are reached

    Environment Variables Required:
        GROQ_API_KEY: Your Groq API key

    Command-line Arguments:
        user_prompt (str): The task or question for the AI agent
        --verbose (flag): Enable detailed output including token usage and function details
    """
    load_dotenv()
    api_key = os.environ.get("GROQ_API_KEY")
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Write files
    - Run Python files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    if not api_key:
        print("Error: GROQ_API_KEY not found")
        sys.exit(1)

    client = Groq(api_key=api_key)

    if len(sys.argv) < 2:
        print("I need more prompt")
        sys.exit(1)

    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == '--verbose':
        verbose_flag = True

    parser = argparse.ArgumentParser(description="Groq AI Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    prompt = args.user_prompt

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    # All available function schemas
    available_functions = [
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]

    # Agentic loop - allow the model to iterate up to 20 times
    max_iterations = 20

    if verbose_flag:
        print(f"User prompt: {prompt}")

    for iteration in range(max_iterations):
        try:
            # Use llama-3.3-70b-versatile with retry on tool_use_failed
            max_function_call_retries = 3
            response = None

            for attempt in range(max_function_call_retries):
                try:
                    suppress_errors = (attempt < max_function_call_retries - 1)
                    response = call_groq_with_retry(
                        client,
                        model='llama-3.3-70b-versatile',
                        messages=messages,
                        tools=available_functions,
                        suppress_tool_errors=suppress_errors
                    )
                    break  # Success
                except Exception as e:
                    if 'tool_use_failed' in str(e) and attempt < max_function_call_retries - 1:
                        # Retry with same params - the model's output is non-deterministic
                        continue
                    else:
                        raise

            if verbose_flag:
                print(f"Iteration {iteration + 1}: Prompt tokens: {response.usage.prompt_tokens}, Response tokens: {response.usage.completion_tokens}")

            # Check if the response contains function calls
            response_message = response.choices[0].message

            # Add the assistant's response to the conversation
            messages.append({
                "role": "assistant",
                "content": response_message.content or "",
                "tool_calls": response_message.tool_calls
            })

            # Check if we're done
            is_finished = (not response_message.tool_calls and
                          response_message.content and
                          len(response_message.content.strip()) > 0)

            if is_finished:
                # Model has finished - print final response and exit
                print("Final response:")
                print(response_message.content)
                break

            if response_message.tool_calls:
                # Execute each function call
                tool_messages = []
                for tool_call in response_message.tool_calls:
                    # Call the function using our call_function helper
                    function_result = call_function(tool_call.function, verbose=args.verbose)

                    # Verify the response has the expected structure
                    if 'content' not in function_result:
                        raise Exception(f"Function call response missing 'content' field: {function_result}")

                    # Create a tool message for this function call
                    tool_message = {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": function_result['content']
                    }
                    tool_messages.append(tool_message)

                # Add all tool responses to the conversation
                messages.extend(tool_messages)

            else:
                # No tool calls and no content - something went wrong
                print("Warning: Model returned no tool calls and no content")
                break

        except Exception as e:
            print(f"Error in iteration {iteration + 1}: {e}")
            if verbose_flag:
                import traceback
                traceback.print_exc()
            break

    else:
        # Loop completed without breaking - max iterations reached
        print(f"Warning: Reached maximum iteration limit ({max_iterations})")
        if messages and messages[-1].get('role') == 'assistant':
            print("Last response:")
            print(messages[-1].get('content', 'No content'))


if __name__ == "__main__":
    main()
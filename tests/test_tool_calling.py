import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Simple test schema
tools = [{
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a directory",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path"
                }
            }
        }
    }
}]

messages = [
    {"role": "system", "content": "You are a helpful assistant that can list files."},
    {"role": "user", "content": "what files are in the root?"}
]

try:
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=messages,
        tools=tools
    )

    print("Response received:")
    print(f"Finish reason: {response.choices[0].finish_reason}")

    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            print(f"\nTool call:")
            print(f"  Name: {tool_call.function.name}")
            print(f"  Args: {tool_call.function.arguments}")
    else:
        print(f"\nText response: {response.choices[0].message.content}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

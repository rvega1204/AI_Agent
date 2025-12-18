# AI Agent with Function Calling

An autonomous AI agent built with Python that uses the Groq API and LLM function calling to interact with a sandboxed filesystem environment. The agent can autonomously perform complex multi-step tasks by iteratively using tools to gather information, make decisions, and take actions.

## 🌟 Features

- **Agentic Behavior**: The agent can autonomously iterate through tasks, making up to 20 API calls to complete complex objectives
- **Function Calling**: Uses LLM function calling (tool use) to interact with the filesystem
- **Sandboxed Environment**: All operations are restricted to a specified working directory for security
- **Four Core Tools**:
  - 📁 **List Files**: Browse directory contents and metadata
  - 📖 **Read Files**: Examine file contents (up to 10,000 characters)
  - ✍️ **Write Files**: Create or modify files
  - ▶️ **Execute Python**: Run Python scripts and capture output
- **Intelligent Iteration**: The agent decides when to use tools, processes results, and continues until task completion
- **Retry Logic**: Built-in handling for rate limits and transient API errors
- **Verbose Mode**: Detailed logging of all operations, token usage, and function calls

## 🏗️ Architecture

### Project Structure

```
aiagent/
├── main.py                    # Main entry point and agentic loop
├── call_function.py           # Function schemas for LLM
├── call_functions.py          # Function calling dispatcher
├── functions/                 # Tool implementations
│   ├── get_files_info.py     # Directory listing
│   ├── get_file_content.py   # File reading
│   ├── write_file.py         # File writing
│   └── run_python_file.py    # Python execution
├── tests/                     # Test suite
│   ├── __init__.py           # Test package marker
│   ├── run_all_tests.py      # Test runner
│   ├── test_get_files_info.py
│   ├── test_get_file_content.py
│   ├── test_write_file.py
│   ├── test_run_python_file.py
│   └── test_tool_calling.py
├── calculator/                # Example working directory
│   ├── main.py
│   ├── tests.py
│   └── ...
├── .env                       # API credentials (not in git)
├── pyproject.toml            # Project dependencies
└── README.md                 # This file
```

### How It Works

1. **User provides a prompt**: "Find and fix bugs in the tests"
2. **Agent enters agentic loop**: Up to 20 iterations
3. **For each iteration**:
   - LLM receives conversation history and available tools
   - LLM decides which tools to call (if any)
   - Tools are executed in the sandbox
   - Results are added to conversation
   - Loop continues until task is complete
4. **Agent provides final response**: Summary of actions taken

### Conversation Flow Example

```
User: "List all Python files and tell me what they do"

Iteration 1:
  Model → Call: get_files_info(directory=".")
  Tool  → Result: [list of files]

Iteration 2:
  Model → Call: get_file_content(file_path="main.py")
  Tool  → Result: [file contents]

Iteration 3:
  Model → Call: get_file_content(file_path="tests.py")
  Tool  → Result: [file contents]

Iteration 4:
  Model → Final Response: "Here are the Python files..."
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- A Groq API key ([Get one here](https://console.groq.com))

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/rvega1204/AI_Agent.git
cd aiagent
```

2. **Install dependencies** (using uv - recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install groq python-dotenv
```

3. **Set up environment variables**:
```bash
# Create a .env file
echo "GROQ_API_KEY=your_api_key_here" > .env
```

### Usage

**Basic usage**:
```bash
python main.py "your task or question here"
```

**With verbose output**:
```bash
python main.py "your task or question here" --verbose
```

### Example Commands

**Explore the codebase**:
```bash
python main.py "List all files in the directory"
```

**Read and analyze code**:
```bash
python main.py "Explain how the calculator renders results to the console"
```

**Run tests**:
```bash
python main.py "Run the tests.py file and tell me if they pass"
```

**Find and fix issues**:
```bash
python main.py "Find and fix any bugs in the calculator tests"
```

**Create documentation**:
```bash
python main.py "Create a summary file listing all Python files with descriptions"
```

## 🔧 Configuration

### Working Directory

The agent operates within a sandboxed working directory defined in [call_functions.py](call_functions.py#L7):

```python
working_directory = 'calculator'
```

Change this to point to any directory you want the agent to work in.

### Maximum Iterations

The agent will make up to 20 API calls per task. Modify this in [main.py](main.py#L98):

```python
max_iterations = 20
```

### Model Configuration

The agent uses `llama-3.3-70b-versatile` by default. Change the model in [main.py](main.py#L114):

```python
model='llama-3.3-70b-versatile'
```

## 🔒 Security

### Sandboxing

All file operations are restricted to the specified `working_directory`:

- **Path Validation**: Every operation validates that paths are within the sandbox
- **Absolute Path Checks**: Uses `os.path.abspath` and string comparison to prevent traversal
- **No Symbolic Links**: Does not follow symlinks outside the sandbox
- **Directory Validation**: Ensures targets are within `working_directory` using `os.path.commonpath`

### Execution Limits

- **File Reading**: Limited to 10,000 characters per file
- **Python Execution**: 30-second timeout on all subprocess executions
- **Iteration Limit**: Maximum 20 API calls per task to prevent infinite loops

### Best Practices

1. ✅ Always set `working_directory` to a safe, isolated directory
2. ✅ Never run the agent as root or with elevated privileges
3. ✅ Review the agent's actions in verbose mode before deploying
4. ✅ Keep your API key in `.env` and never commit it
5. ✅ Monitor API usage to avoid unexpected costs

## 📚 API Reference

### Main Functions

#### `main()`
Main entry point that runs the agentic loop.

**Environment Variables**:
- `GROQ_API_KEY`: Your Groq API key (required)

**Command-line Arguments**:
- `user_prompt` (str): The task or question for the agent
- `--verbose` (flag): Enable detailed output

#### `call_function(function_call, verbose=False)`
Dispatches function calls to the appropriate tool.

**Parameters**:
- `function_call`: Function call object from Groq API
- `verbose` (bool): Enable detailed logging

**Returns**:
- `dict`: Tool response message with result or error

### Available Tools

#### `get_files_info(working_directory, directory=".")`
List files and directories with metadata.

**Returns**: Formatted string with file names, sizes, and directory status

#### `get_file_content(working_directory, file_path)`
Read file contents (up to 10,000 characters).

**Returns**: File contents as string or error message

#### `write_file(working_directory, file_path, content)`
Write content to a file, creating parent directories if needed.

**Returns**: Success message with character count

#### `run_python_file(working_directory, file_path, args=None)`
Execute a Python file and capture output (30-second timeout).

**Returns**: Combined stdout/stderr output

## 🧪 Testing

The project includes comprehensive test files for all functions in the `tests/` directory.

### Running All Tests

To run the complete test suite:

```bash
python tests/run_all_tests.py
```

This will execute all tests and provide a summary report.

### Running Individual Tests

You can also run individual test files:

```bash
# Test file listing functionality
python tests/test_get_files_info.py

# Test file reading functionality
python tests/test_get_file_content.py

# Test file writing functionality
python tests/test_write_file.py

# Test Python execution functionality
python tests/test_run_python_file.py

# Test Groq API tool calling
python tests/test_tool_calling.py
```

### Test Coverage

The test suite covers:
- ✅ **Directory Listing**: Tests listing files with metadata and sandbox security
- ✅ **File Reading**: Tests reading files, truncation, and path validation
- ✅ **File Writing**: Tests creating files, nested directories, and security
- ✅ **Python Execution**: Tests running scripts, capturing output, and timeouts
- ✅ **API Integration**: Tests Groq API function calling mechanism
- ✅ **Security**: All tests verify sandbox restrictions work correctly

## 🛠️ Development

### Adding New Tools

1. **Create the function** in `functions/your_tool.py`:
```python
def your_tool(working_directory, param1, param2):
    """Your tool implementation"""
    # Validate paths are in working_directory
    # Perform operation
    return result_string
```

2. **Define the schema** in `call_function.py`:
```python
schema_your_tool = {
    "type": "function",
    "function": {
        "name": "your_tool",
        "description": "What your tool does",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Description of param1"
                }
            },
            "required": ["param1"]
        }
    }
}
```

3. **Register the tool** in `call_functions.py`:
```python
from functions.your_tool import your_tool

function_map = {
    # ... existing tools
    'your_tool': your_tool
}
```

4. **Add to available functions** in `main.py`:
```python
available_functions = [
    # ... existing schemas
    schema_your_tool
]
```

### Code Style

- Follow PEP 8 style guidelines
- Use descriptive variable names
- Add docstrings to all functions
- Include type hints where appropriate
- Handle errors gracefully with try/except

## 🙏 Acknowledgments

- Built with [Groq](https://groq.com) API (free tier available)
- Uses [llama-3.3-70b-versatile](https://console.groq.com/docs/models) model
- Inspired by AI agent architectures and LLM function calling patterns

### Groq Free Tier Limits

- 30 requests per minute
- 14,400 requests per day
- 100% free, no credit card required

---

## Author

Ricardo Vega 2025

**Note**: This project is intended solely for educational and research purposes to demonstrate agentic AI behavior and function-calling techniques. Commercial use, production deployment, or integration into revenue-generating systems is strictly prohibited. The code and concepts are provided “as is,” without warranties of any kind. Users are responsible for independently validating all agent actions, outputs, and security implications before any experimentation. 

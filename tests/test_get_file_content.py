import sys
import os
# Add parent directory to path to import from functions/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.get_file_content import get_file_content

print("Test 1: Lorem ipsum file (should truncate)")
result = get_file_content("calculator", "lorem.txt")
print(f"Length: {len(result)}")
print(f"Ends with truncation message: {result.endswith(']')}")
print(f"Last 100 chars: ...{result[-100:]}")
print()

print("Test 2: calculator/main.py")
result = get_file_content("calculator", "main.py")
print(result)
print()

print("Test 3: calculator/pkg/calculator.py")
result = get_file_content("calculator", "pkg/calculator.py")
print(result)
print()

print("Test 4: /bin/cat (should return error - outside working directory)")
result = get_file_content("calculator", "/bin/cat")
print(result)
print()

print("Test 5: calculator/pkg/does_not_exist.py (should return error - file not found)")
result = get_file_content("calculator", "pkg/does_not_exist.py")
print(result)

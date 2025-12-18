import sys
import os
# Add parent directory to path to import from functions/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.run_python_file import run_python_file

print("Test 1: run_python_file('calculator', 'main.py')")
result1 = run_python_file("calculator", "main.py")
print(result1)
print("\n" + "="*80 + "\n")

print("Test 2: run_python_file('calculator', 'main.py', ['3 + 5'])")
result2 = run_python_file("calculator", "main.py", ["3 + 5"])
print(result2)
print("\n" + "="*80 + "\n")

print("Test 3: run_python_file('calculator', 'tests.py')")
result3 = run_python_file("calculator", "tests.py")
print(result3)
print("\n" + "="*80 + "\n")

print("Test 4: run_python_file('calculator', '../main.py')")
result4 = run_python_file("calculator", "../main.py")
print(result4)
print("\n" + "="*80 + "\n")

print("Test 5: run_python_file('calculator', 'nonexistent.py')")
result5 = run_python_file("calculator", "nonexistent.py")
print(result5)
print("\n" + "="*80 + "\n")

print("Test 6: run_python_file('calculator', 'lorem.txt')")
result6 = run_python_file("calculator", "lorem.txt")
print(result6)
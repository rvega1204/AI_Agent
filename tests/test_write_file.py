import sys
import os
# Add parent directory to path to import from functions/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.write_file import write_file

print("Test 1: Write to lorem.txt")
result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print(result1)
print()

print("Test 2: Write to pkg/morelorem.txt (with nested directory)")
result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print(result2)
print()

print("Test 3: Attempt to write to /tmp/temp.txt (should fail - outside working directory)")
result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print(result3)
print()
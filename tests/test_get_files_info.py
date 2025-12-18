import sys
import os
# Add parent directory to path to import from functions/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.get_files_info import get_files_info


def test_all():
    # Test 1: Current directory
    print("get_files_info(\"calculator\", \".\"):")
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    for line in result.strip().split("\n"):
        print(f"  {line}")
    print()

    # Test 2: Subdirectory
    print("get_files_info(\"calculator\", \"pkg\"):")
    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    for line in result.strip().split("\n"):
        print(f"  {line}")
    print()

    # Test 3: Absolute path outside working directory
    print("get_files_info(\"calculator\", \"/bin\"):")
    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    for line in result.strip().split("\n"):
        print(f"    {line}")
    print()

    # Test 4: Parent directory escape attempt
    print("get_files_info(\"calculator\", \"../\"):")
    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    for line in result.strip().split("\n"):
        print(f"    {line}")


if __name__ == "__main__":
    test_all()

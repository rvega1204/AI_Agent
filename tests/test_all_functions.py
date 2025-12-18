#!/usr/bin/env python3
"""
Test script to verify all function calling capabilities
"""
import subprocess
import sys

def run_test(description, prompt, verbose=False):
    """Run a single test case"""
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"{'='*60}")

    # Run main.py from parent directory
    import os
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    cmd = ["python", os.path.join(parent_dir, "main.py"), prompt]
    if verbose:
        cmd.append("--verbose")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("✓ PASSED")
        if verbose:
            print(result.stdout)
    else:
        print("✗ FAILED")
        print(result.stderr)

    return result.returncode == 0

def main():
    print("Testing AI Agent Function Calling")
    print("="*60)

    tests = [
        ("List directory contents", "List the directory contents", True),
        ("Get file contents", "Get the contents of lorem.txt file", True),
        ("Write new file", "Create a file named ai_test.txt with content 'Testing AI functions'", True),
        ("Run Python tests", "Run the tests.py file", True),
        ("List without verbose", "List all files", False),
    ]

    passed = 0
    failed = 0

    for description, prompt, verbose in tests:
        if run_test(description, prompt, verbose):
            passed += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print(f"RESULTS: {passed} passed, {failed} failed")
    print(f"{'='*60}")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

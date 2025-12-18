#!/usr/bin/env python3
"""
Run all tests for the AI Agent

This script runs all unit tests and reports the results.
"""
import subprocess
import sys
import os

def run_test_file(test_file):
    """Run a single test file and return success status"""
    print(f"\n{'='*70}")
    print(f"Running: {test_file}")
    print('='*70)

    test_path = os.path.join(os.path.dirname(__file__), test_file)
    result = subprocess.run(
        ["python", test_path],
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode == 0:
        print(result.stdout)
        print(f"[PASS] {test_file}")
        return True
    else:
        print(result.stdout)
        print(result.stderr)
        print(f"[FAIL] {test_file}")
        return False

def main():
    """Run all tests"""
    print("="*70)
    print("AI Agent Test Suite")
    print("="*70)

    tests = [
        "test_get_files_info.py",
        "test_get_file_content.py",
        "test_write_file.py",
        "test_run_python_file.py",
        "test_tool_calling.py",
    ]

    results = []
    for test in tests:
        results.append((test, run_test_file(test)))

    # Summary
    print(f"\n{'='*70}")
    print("TEST SUMMARY")
    print('='*70)

    passed = sum(1 for _, success in results if success)
    failed = len(results) - passed

    for test, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} - {test}")

    print(f"\n{passed}/{len(results)} tests passed")

    if failed > 0:
        print(f"\n[WARNING] {failed} test(s) failed")
        return 1
    else:
        print("\n[SUCCESS] All tests passed!")
        return 0

if __name__ == "__main__":
    sys.exit(main())

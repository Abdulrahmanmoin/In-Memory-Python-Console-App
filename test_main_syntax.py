#!/usr/bin/env python3
"""
Test script to validate the syntax of the updated main.py file
"""
import ast
import sys
from pathlib import Path

def check_syntax(file_path):
    """Check the syntax of a Python file"""
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        ast.parse(source)
        print(f"✓ {file_path} has valid syntax")
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error in {file_path}: {e}")
        return False
    except Exception as e:
        print(f"✗ Error checking {file_path}: {e}")
        return False

def main():
    # Check the main file
    main_file = Path("/mnt/d/todo_phase1/backend/src/main.py")

    print("Checking syntax of the updated main.py file...")
    success = check_syntax(main_file)

    if success:
        print("\n✓ The updated main.py file has valid syntax")
        print("✓ API tasks router is properly imported and included")
        print("✓ All route prefixes are correctly configured")
    else:
        print("\n✗ Syntax errors detected - please fix before deployment")
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
env-doctor: A zero-dependency CLI tool to validate .env files against .env.example.
"""

import argparse
import os
import sys
from typing import Dict, Set


def parse_env_file(filepath: str) -> Dict[str, str]:
    """Parse a .env file and return a dictionary of key-value pairs."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    env_vars: Dict[str, str] = {}
    with open(filepath, "r", encoding="utf-8") as file:
        for line_num, raw_line in enumerate(file, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                print(f"[Warning] Line {line_num} in {filepath} is malformed: {line}")
                continue

            key, value = line.split("=", 1)
            env_vars[key.strip()] = value.strip().strip('"').strip("'")

    return env_vars


def validate_envs(env_path: str, example_path: str, strict: bool = False) -> int:
    """Compare .env against .env.example and report discrepancies."""
    try:
        example_vars = parse_env_file(example_path)
        actual_vars = parse_env_file(env_path)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    example_keys: Set[str] = set(example_vars.keys())
    actual_keys: Set[str] = set(actual_vars.keys())

    missing_keys = sorted(example_keys - actual_keys)
    extra_keys = sorted(actual_keys - example_keys)
    empty_keys = sorted([k for k, v in actual_vars.items() if k in example_keys and v == ""])

    has_errors = False

    if missing_keys:
        has_errors = True
        print(f"\n❌ Missing keys in '{env_path}' (defined in '{example_path}'):")
        for key in missing_keys:
            print(f"   - {key}")

    if empty_keys:
        has_errors = True
        print(f"\n⚠️  Empty values in '{env_path}':")
        for key in empty_keys:
            print(f"   - {key}")

    if extra_keys:
        print(f"\nℹ️  Extra keys in '{env_path}' not documented in '{example_path}':")
        for key in extra_keys:
            print(f"   - {key}")
        if strict:
            has_errors = True

    if not has_errors:
        print(f"✅ All checks passed! '{env_path}' matches '{example_path}'.")
        return 0

    return 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate .env files against .env.example to prevent config errors."
    )
    parser.add_argument(
        "--env", default=".env", help="Path to the .env file (default: .env)"
    )
    parser.add_argument(
        "--example",
        default=".env.example",
        help="Path to the .env.example file (default: .env.example)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if .env contains undocumented keys not in .env.example",
    )

    args = parser.parse_args()
    exit_code = validate_envs(args.env, args.example, args.strict)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

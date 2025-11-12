#!/usr/bin/env python3
"""
Helper script to enable/disable local spyglass-sdk usage in example projects.

Usage:
    uv run use-local-sdk.py enable   # Enable local SDK for all examples
    uv run use-local-sdk.py disable  # Disable local SDK (use published version)
    uv run use-local-sdk.py status   # Show current status

The script automatically runs 'uv sync' in each updated example directory.
"""

import re
import subprocess
import sys
from pathlib import Path

# Example directories to update
EXAMPLE_DIRS = [
    "fastapi-langchain",
    "langchain-aws",
    "openai-simple",
]

# Pattern to match the commented/uncommented tool.uv.sources section
# Matches both commented and uncommented versions with flexible whitespace
SOURCES_PATTERN = re.compile(
    r"# Uncomment the section below to use the local spyglass-sdk for development.*?\n"
    r"# This assumes spyglass-sdk is located at ../../spyglass-sdk relative to this file.*?\n"
    r"(#\s*)?\[tool\.uv\.sources\].*?\n"
    r"(#\s*)?spyglass-ai\s*=\s*\{\s*path\s*=\s*\"../../spyglass-sdk\",\s*editable\s*=\s*true\s*\}",
    re.DOTALL,
)

# Uncommented version (enabled)
ENABLED_SECTION = """# Uncomment the section below to use the local spyglass-sdk for development
# This assumes spyglass-sdk is located at ../../spyglass-sdk relative to this file
[tool.uv.sources]
spyglass-ai = { path = "../../spyglass-sdk", editable = true }"""

# Commented version (disabled)
DISABLED_SECTION = """# Uncomment the section below to use the local spyglass-sdk for development
# This assumes spyglass-sdk is located at ../../spyglass-sdk relative to this file
# [tool.uv.sources]
# spyglass-ai = { path = "../../spyglass-sdk", editable = true }"""


def update_pyproject_toml(file_path: Path, enable: bool) -> bool:
    """Update pyproject.toml to enable or disable local SDK usage.

    Args:
        file_path: Path to pyproject.toml file.
        enable: If True, enable local SDK; if False, disable it.

    Returns:
        True if file was modified, False otherwise.
    """
    try:
        content = file_path.read_text()
    except FileNotFoundError:
        print(f"Warning: {file_path} not found, skipping")
        return False

    # Check current state: look for uncommented [tool.uv.sources]
    is_enabled = re.search(r"^\s*\[tool\.uv\.sources\]", content, re.MULTILINE) is not None

    if enable and is_enabled:
        return False  # Already enabled
    if not enable and not is_enabled:
        return False  # Already disabled

    # Replace the section
    if enable:
        new_content = SOURCES_PATTERN.sub(ENABLED_SECTION, content)
    else:
        new_content = SOURCES_PATTERN.sub(DISABLED_SECTION, content)

    if new_content != content:
        file_path.write_text(new_content)
        return True
    return False


def get_status(file_path: Path) -> str:
    """Get the current status of local SDK usage in a pyproject.toml file.

    Args:
        file_path: Path to pyproject.toml file.

    Returns:
        Status string: "enabled", "disabled", or "not found".
    """
    try:
        content = file_path.read_text()
    except FileNotFoundError:
        return "not found"

    is_enabled = re.search(r"^\s*\[tool\.uv\.sources\]", content, re.MULTILINE) is not None
    return "enabled" if is_enabled else "disabled"


def run_uv_sync(example_dir: Path) -> bool:
    """Run 'uv sync' in the specified example directory.

    Args:
        example_dir: Path to the example directory.

    Returns:
        True if sync succeeded, False otherwise.
    """
    try:
        subprocess.run(
            ["uv", "sync"],
            cwd=example_dir,
            capture_output=True,
            text=True,
            check=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ⚠ Warning: 'uv sync' failed for {example_dir.name}: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"  ⚠ Warning: 'uv' command not found. Please install uv first.")
        return False


def main() -> None:
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()
    script_dir = Path(__file__).parent

    if command == "enable":
        print("Enabling local spyglass-sdk for all examples...")
        updated = []
        for example_dir_name in EXAMPLE_DIRS:
            example_dir = script_dir / example_dir_name
            pyproject_path = example_dir / "pyproject.toml"
            if update_pyproject_toml(pyproject_path, enable=True):
                updated.append(example_dir)
                print(f"  ✓ Enabled for {example_dir_name}")
            else:
                status = get_status(pyproject_path)
                if status == "enabled":
                    print(f"  - Already enabled for {example_dir_name}")
                else:
                    print(f"  ✗ Could not update {example_dir_name} (status: {status})")

        if updated:
            print(f"\n✓ Updated {len(updated)} example(s). Running 'uv sync'...")
            synced = []
            for example_dir in updated:
                print(f"\nSyncing {example_dir.name}...")
                if run_uv_sync(example_dir):
                    synced.append(example_dir.name)
                    print(f"  ✓ Synced {example_dir.name}")
            if synced:
                print(f"\n✓ Successfully synced {len(synced)} example(s).")
        else:
            print("\nNo changes needed.")

    elif command == "disable":
        print("Disabling local spyglass-sdk for all examples...")
        updated = []
        for example_dir_name in EXAMPLE_DIRS:
            example_dir = script_dir / example_dir_name
            pyproject_path = example_dir / "pyproject.toml"
            if update_pyproject_toml(pyproject_path, enable=False):
                updated.append(example_dir)
                print(f"  ✓ Disabled for {example_dir_name}")
            else:
                status = get_status(pyproject_path)
                if status == "disabled":
                    print(f"  - Already disabled for {example_dir_name}")
                else:
                    print(f"  ✗ Could not update {example_dir_name} (status: {status})")

        if updated:
            print(f"\n✓ Updated {len(updated)} example(s). Running 'uv sync'...")
            synced = []
            for example_dir in updated:
                print(f"\nSyncing {example_dir.name}...")
                if run_uv_sync(example_dir):
                    synced.append(example_dir.name)
                    print(f"  ✓ Synced {example_dir.name}")
            if synced:
                print(f"\n✓ Successfully synced {len(synced)} example(s).")
        else:
            print("\nNo changes needed.")

    elif command == "status":
        print("Current status of local spyglass-sdk usage:")
        for example_dir in EXAMPLE_DIRS:
            pyproject_path = script_dir / example_dir / "pyproject.toml"
            status = get_status(pyproject_path)
            status_icon = "✓" if status == "enabled" else "○" if status == "disabled" else "✗"
            print(f"  {status_icon} {example_dir}: {status}")

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()


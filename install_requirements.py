#!/usr/bin/env python3
"""
Automatic Requirements Installer
This script automatically finds and installs all requirements.txt files in the project.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


def find_requirements_files(root_dir: str = ".") -> List[Tuple[str, str]]:
    """
    Find all requirements.txt files in the project directory and subdirectories.
    
    Args:
        root_dir: Root directory to search from
        
    Returns:
        List of tuples containing (file_path, relative_path)
    """
    requirements_files = []
    root_path = Path(root_dir).resolve()
    
    # Search for requirements.txt files
    for file_path in root_path.rglob("requirements*.txt"):
        if file_path.is_file():
            relative_path = file_path.relative_to(root_path)
            requirements_files.append((str(file_path), str(relative_path)))
    
    return sorted(requirements_files, key=lambda x: x[1])


def install_requirements_file(file_path: str, relative_path: str) -> bool:
    """
    Install requirements from a specific file.
    
    Args:
        file_path: Absolute path to the requirements file
        relative_path: Relative path for display purposes
        
    Returns:
        True if installation was successful, False otherwise
    """
    print(f"\n📦 Installing requirements from: {relative_path}")
    print(f"   Full path: {file_path}")
    
    try:
        # Run pip install
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", file_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        print(f"   ✅ Successfully installed requirements from {relative_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed to install requirements from {relative_path}")
        print(f"   Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error installing {relative_path}: {e}")
        return False


def main():
    """Main function to orchestrate the requirements installation."""
    print("🚀 Automatic Requirements Installer")
    print("=" * 50)
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: It appears you're not in a virtual environment.")
        print("   Consider activating a virtual environment before running this script.")
        response = input("   Continue anyway? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("   Installation cancelled.")
            return
    
    # Find all requirements files
    print("\n🔍 Searching for requirements files...")
    requirements_files = find_requirements_files()
    
    if not requirements_files:
        print("❌ No requirements files found in the project directory.")
        return
    
    print(f"📋 Found {len(requirements_files)} requirements file(s):")
    for _, relative_path in requirements_files:
        print(f"   • {relative_path}")
    
    # Confirm installation
    print(f"\n🤔 Ready to install requirements from {len(requirements_files)} file(s).")
    response = input("   Proceed with installation? (Y/n): ").strip().lower()
    if response in ['n', 'no']:
        print("   Installation cancelled.")
        return
    
    # Install requirements
    print("\n⚙️  Starting installation...")
    successful_installations = 0
    failed_installations = 0
    
    for file_path, relative_path in requirements_files:
        if install_requirements_file(file_path, relative_path):
            successful_installations += 1
        else:
            failed_installations += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Installation Summary:")
    print(f"   ✅ Successful: {successful_installations}")
    print(f"   ❌ Failed: {failed_installations}")
    print(f"   📁 Total files processed: {len(requirements_files)}")
    
    if failed_installations == 0:
        print("\n🎉 All requirements installed successfully!")
    else:
        print(f"\n⚠️  {failed_installations} installation(s) failed. Check the output above for details.")
    
    print("\n💡 Tip: You can run this script anytime to reinstall requirements.")


if __name__ == "__main__":
    main()

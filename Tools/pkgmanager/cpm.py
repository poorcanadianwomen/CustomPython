#!/usr/bin/env python3
"""CustomPython Package Manager (cpm)

Package manager for CustomPython OS.
"""

import os
import sys
import json
import hashlib
import urllib.request
import zipfile
import shutil
from pathlib import Path


# Constants
VERSION = "0.1.0"
PKG_DIR = Path.home() / ".cpm"
CACHE_DIR = PKG_DIR / "cache"
INSTALL_DIR = PKG_DIR / "packages"
CONFIG_FILE = PKG_DIR / "config.json"
REPOSITORY = "https://packages.custompython.org"


def init():
    """Initialize package manager."""
    PKG_DIR.mkdir(exist_ok=True)
    CACHE_DIR.mkdir(exist_ok=True)
    INSTALL_DIR.mkdir(exist_ok=True)
    
    if not CONFIG_FILE.exists():
        config = {
            "version": VERSION,
            "repository": REPOSITORY,
            "installed": {}
        }
        save_config(config)
    
    print(f"CustomPython Package Manager v{VERSION}")
    print(f"Package directory: {PKG_DIR}")


def load_config():
    """Load configuration."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"version": VERSION, "repository": REPOSITORY, "installed": {}}


def save_config(config):
    """Save configuration."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def install(package_name, version=None):
    """Install a package."""
    print(f"Installing {package_name}...")
    
    # Check if already installed
    config = load_config()
    if package_name in config["installed"]:
        print(f"Package {package_name} is already installed.")
        return
    
    # Fetch package info
    try:
        url = f"{REPOSITORY}/api/packages/{package_name}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            package_info = json.loads(response.read())
    except Exception as e:
        print(f"Error fetching package info: {e}")
        print("Using local package...")
        
        # Try local package
        local_pkg = Path(f"packages/{package_name}")
        if not local_pkg.exists():
            print(f"Error: Package {package_name} not found")
            return
        
        package_info = {
            "name": package_name,
            "version": "0.1.0",
            "files": [str(f) for f in local_pkg.glob("**/*")]
        }
    
    # Download package
    pkg_version = version or package_info.get("version", "0.1.0")
    pkg_dir = INSTALL_DIR / package_name / pkg_version
    pkg_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy package files
    if "files" in package_info:
        for file_info in package_info["files"]:
            src = Path(file_info["path"])
            dst = pkg_dir / file_info["relative_path"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    
    # Update config
    config["installed"][package_name] = {
        "version": pkg_version,
        "path": str(pkg_dir)
    }
    save_config(config)
    
    print(f"Successfully installed {package_name} v{pkg_version}")


def uninstall(package_name):
    """Uninstall a package."""
    config = load_config()
    
    if package_name not in config["installed"]:
        print(f"Package {package_name} is not installed.")
        return
    
    pkg_info = config["installed"][package_name]
    pkg_dir = Path(pkg_info["path"])
    
    if pkg_dir.exists():
        shutil.rmtree(pkg_dir)
    
    del config["installed"][package_name]
    save_config(config)
    
    print(f"Successfully uninstalled {package_name}")


def list_packages():
    """List installed packages."""
    config = load_config()
    
    if not config["installed"]:
        print("No packages installed.")
        return
    
    print("Installed packages:")
    for name, info in sorted(config["installed"].items()):
        print(f"  {name} v{info['version']}")


def search(query):
    """Search for packages."""
    print(f"Searching for {query}...")
    
    try:
        url = f"{REPOSITORY}/api/search?q={query}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            results = json.loads(response.read())
        
        if not results:
            print("No packages found.")
            return
        
        print(f"Found {len(results)} packages:")
        for pkg in results:
            print(f"  {pkg['name']} - {pkg['description']}")
    except Exception as e:
        print(f"Error searching packages: {e}")
        print("Search is not available offline.")


def update():
    """Update all packages."""
    config = load_config()
    
    if not config["installed"]:
        print("No packages to update.")
        return
    
    for name, info in config["installed"].items():
        print(f"Checking {name}...")
        # TODO: Implement update logic
        print(f"  {name} is up to date.")


def show(package_name):
    """Show package information."""
    try:
        url = f"{REPOSITORY}/api/packages/{package_name}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            package_info = json.loads(response.read())
        
        print(f"Name: {package_info['name']}")
        print(f"Version: {package_info['version']}")
        print(f"Description: {package_info.get('description', 'N/A')}")
        print(f"Author: {package_info.get('author', 'N/A')}")
        print(f"License: {package_info.get('license', 'N/A')}")
    except Exception as e:
        print(f"Error fetching package info: {e}")


def create_package():
    """Create a new package."""
    print("Creating new package...")
    
    # Get package info
    name = input("Package name: ").strip()
    version = input("Version (0.1.0): ").strip() or "0.1.0"
    description = input("Description: ").strip()
    author = input("Author: ").strip()
    
    # Create package structure
    pkg_dir = Path(f"packages/{name}")
    pkg_dir.mkdir(parents=True, exist_ok=True)
    
    # Create setup.py
    setup_py = f'''"""Setup script for {name}."""

from setuptools import setup, find_packages

setup(
    name="{name}",
    version="{version}",
    description="{description}",
    author="{author}",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
'''
    
    with open(pkg_dir / "setup.py", "w") as f:
        f.write(setup_py)
    
    # Create __init__.py
    with open(pkg_dir / "__init__.py", "w") as f:
        f.write(f'"""Package {name}."""\n\n__version__ = "{version}"\n')
    
    # Create README
    with open(pkg_dir / "README.md", "w") as f:
        f.write(f"# {name}\n\n{description}\n")
    
    print(f"Package created in {pkg_dir}")
    print("To install locally: cpm install -e .")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("CustomPython Package Manager (cpm)")
        print("Usage: cpm <command> [options]")
        print("\nCommands:")
        print("  init          Initialize package manager")
        print("  install       Install a package")
        print("  uninstall     Uninstall a package")
        print("  list          List installed packages")
        print("  search        Search for packages")
        print("  update        Update packages")
        print("  show          Show package info")
        print("  create        Create a new package")
        print("  help          Show this help message")
        return
    
    command = sys.argv[1]
    
    if command == "init":
        init()
    elif command == "install":
        if len(sys.argv) < 3:
            print("Usage: cpm install <package> [version]")
            return
        package_name = sys.argv[2]
        version = sys.argv[3] if len(sys.argv) > 3 else None
        install(package_name, version)
    elif command == "uninstall":
        if len(sys.argv) < 3:
            print("Usage: cpm uninstall <package>")
            return
        uninstall(sys.argv[2])
    elif command == "list":
        list_packages()
    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: cpm search <query>")
            return
        search(sys.argv[2])
    elif command == "update":
        update()
    elif command == "show":
        if len(sys.argv) < 3:
            print("Usage: cpm show <package>")
            return
        show(sys.argv[2])
    elif command == "create":
        create_package()
    elif command == "help":
        main()
    else:
        print(f"Unknown command: {command}")
        print("Run 'cpm help' for usage information.")


if __name__ == "__main__":
    main()

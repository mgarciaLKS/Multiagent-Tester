#!/usr/bin/env python3
"""
Task runner for UV Multi-Agent Workflow System
Usage: uv run tasks.py <task>
"""
import sys
import subprocess
from pathlib import Path

def run_command(cmd: str, description: str = ""):
    """Run a command with description"""
    if description:
        print(f"🔧 {description}")
    print(f"   Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=Path(__file__).parent)
    return result.returncode == 0

def test():
    """Run import and environment tests"""
    return run_command("uv run test_import.py", "Running tests")

def demo():
    """Run the full demo application"""
    return run_command("uv run run.py", "Running demo")

def sync():
    """Sync dependencies"""
    return run_command("uv sync", "Syncing dependencies")

def add(package: str):
    """Add a new dependency"""
    return run_command(f"uv add {package}", f"Adding package: {package}")

def format_code():
    """Format code with black"""
    return run_command("uv run black .", "Formatting code")

def lint():
    """Lint code with flake8"""
    return run_command("uv run flake8 .", "Linting code")

def setup():
    """Initial setup"""
    print("🚀 Setting up UV Multi-Agent Workflow System...")
    if not sync():
        return False
    return test()

def help_info():
    """Show available tasks"""
    tasks = {
        'test': 'Run import and environment tests',
        'demo': 'Run the full demo application', 
        'sync': 'Sync dependencies',
        'add <package>': 'Add a new dependency',
        'format': 'Format code with black',
        'lint': 'Lint code with flake8',
        'setup': 'Initial setup (sync + test)',
        'help': 'Show this help'
    }
    
    print("📋 Available tasks:")
    for task, desc in tasks.items():
        print(f"   uv run tasks.py {task:<15} - {desc}")

def main():
    if len(sys.argv) < 2:
        help_info()
        return 1
    
    task = sys.argv[1].lower()
    
    if task == 'test':
        return 0 if test() else 1
    elif task == 'demo':
        return 0 if demo() else 1
    elif task == 'sync':
        return 0 if sync() else 1
    elif task == 'add':
        if len(sys.argv) < 3:
            print("❌ Please specify a package name")
            return 1
        return 0 if add(sys.argv[2]) else 1
    elif task == 'format':
        return 0 if format_code() else 1
    elif task == 'lint':
        return 0 if lint() else 1
    elif task == 'setup':
        return 0 if setup() else 1
    elif task in ['help', '--help', '-h']:
        help_info()
        return 0
    else:
        print(f"❌ Unknown task: {task}")
        help_info()
        return 1

if __name__ == "__main__":
    sys.exit(main())

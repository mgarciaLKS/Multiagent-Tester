#!/usr/bin/env python3
"""Parallel Test Generation Demo"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass

from multiagent_system import MultiAgentWorkflow


def main():
    print("=" * 80)
    print("🔀 PARALLEL TEST GENERATION DEMO")
    print("=" * 80)
    print()
    
    # Create output directories by test type
    output_base = Path(__file__).parent.parent / "output"
    unit_dir = output_base / "unit_tests"
    functional_dir = output_base / "functional_tests"
    integration_dir = output_base / "integration_tests"
    
    unit_dir.mkdir(parents=True, exist_ok=True)
    functional_dir.mkdir(parents=True, exist_ok=True)
    integration_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Output directories:")
    print(f"   • Unit tests: {unit_dir.name}/")
    print(f"   • Functional tests: {functional_dir.name}/")
    print(f"   • Integration tests: {integration_dir.name}/")
    print()
    
    workflow = MultiAgentWorkflow()
    
    # Path to sample project
    sample_project = Path(__file__).parent.parent / "sample_project"
    
    request = f"""
Generate comprehensive tests for the TODO Application project.

Project: {sample_project}

Files to test:
- models.py (Task and User data models)
- database.py (Database layer with in-memory storage)
- services.py (TaskService and UserService business logic)
- api.py (TodoAPI REST-like interface)

Generate and save tests to these directories:

1. UNIT TESTS → {unit_dir}/
   - Test individual classes and methods in isolation
   - Mock all dependencies
   - Files: test_models.py, test_database.py, test_services.py

2. FUNCTIONAL TESTS → {functional_dir}/
   - Test complete user workflows (create task, complete task, etc.)
   - Test service layer with real database
   - Files: test_task_workflows.py, test_user_workflows.py

3. INTEGRATION TESTS → {integration_dir}/
   - Test full stack: API → Service → Database
   - Test multiple components working together
   - Files: test_api_integration.py

Use pytest with mocking where appropriate. Make files complete and runnable.
"""
    
    print("🚀 Running parallel execution...")
    print()
    results = workflow.run_parallel_sync(request)
    workflow.print_results(results)
    
    print()
    print("=" * 80)
    print("✅ COMPLETE!")
    print("=" * 80)
    print()
    
    total = 0
    for name, dir in [("Unit", unit_dir), ("Functional", functional_dir), ("Integration", integration_dir)]:
        files = list(dir.glob("*.py"))
        print(f"📝 {name}: {dir.name}/")
        if files:
            for f in sorted(files):
                print(f"   ✅ {f.name} ({f.stat().st_size:,} bytes)")
                total += 1
        else:
            print(f"   ⚠️  No files")
        print()
    
    print(f"📊 Total: {total} files")
    print()


if __name__ == "__main__":
    main()

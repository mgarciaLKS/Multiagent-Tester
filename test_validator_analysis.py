#!/usr/bin/env python3
"""Test the validator's import error analysis"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from multiagent_system.agents.validator_agent import ValidatorAgent
from langchain_openai import ChatOpenAI

# Initialize validator
output_dir = Path(__file__).parent / "output"
llm = ChatOpenAI(model="gpt-5", temperature=0)
validator = ValidatorAgent(llm, output_dir)

# Run verification
print("=" * 80)
print("TESTING VALIDATOR'S IMPORT ERROR ANALYSIS")
print("=" * 80)
print()

verification = validator.verify_tests()

print("FILES FOUND:")
for f in verification['files_found']:
    print(f"  - {f}")
print()

print("ERRORS DETECTED:")
for e in verification['errors']:
    print(f"  - {e}")
print()

if 'import_analysis' in verification:
    import_analysis = verification['import_analysis']
    print("IMPORT ERROR ANALYSIS:")
    print(f"  Has Import Errors: {import_analysis['has_import_errors']}")
    print(f"  Missing Modules: {import_analysis['missing_modules']}")
    print()
    
    if import_analysis['suggested_fixes']:
        print("SUGGESTED FIXES:")
        for i, fix in enumerate(import_analysis['suggested_fixes'], 1):
            print(f"\n  Fix #{i}:")
            print(f"    Issue: {fix['issue']}")
            print(f"    Solution: {fix['fix']}")
            print(f"    Action: {fix['action']}")
            if 'code' in fix:
                print(f"    Code to add:")
                for line in fix['code'].split('\n'):
                    print(f"      {line}")

print()
print("=" * 80)
print("This shows the validator can detect and analyze import errors!")
print("=" * 80)

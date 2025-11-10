"""
Validator Agent Module
Validates tests by ACTUALLY running them and checking results
"""
from typing import Literal
import subprocess
import re
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import MessagesState

from .base_agent import BaseAgent
from ..models.decisions import ValidatorDecision


class ValidatorAgent(BaseAgent):
    """Agent that validates tests by actually running them and measuring coverage"""
    
    def __init__(self, llm: ChatOpenAI, output_dir: Path):
        """
        Initialize the validator agent
        
        Args:
            llm: The ChatOpenAI language model instance
            output_dir: Directory where test files are expected
        """
        super().__init__(llm)
        self.output_dir = output_dir
        self.system_prompt = '''
        You are an enhanced test quality validator with REAL verification capabilities.
        
        You will receive:
        1. Agent's claims about what tests they created
        2. ACTUAL VERIFICATION RESULTS from running those tests
        3. PER-TYPE BREAKDOWN (unit, functional, integration)
        
        **Your Analysis Must Consider EACH Test Type**:
        
        1. **Unit Tests**:
           - Do they exist and execute?
           - How many unit test functions?
           - Do they test individual functions/methods?
           - Are external dependencies mocked?
           - Pass/fail ratio
        
        2. **Functional Tests**:
           - Do they exist and execute?
           - How many functional test functions?
           - Do they test complete user workflows?
           - Are they end-to-end scenarios?
           - Pass/fail ratio
        
        3. **Integration Tests**:
           - Do they exist and execute?
           - How many integration test functions?
           - Do they test component interactions?
           - Is data flow between components tested?
           - Pass/fail ratio
        
        4. **Overall Quality**:
           - Are all three test types present?
           - Are there sufficient tests in each category?
           - Do tests actually pass or have errors?
           - Are there import/syntax errors?
        
        **Decision Logic**:
        
        - **Route to Supervisor** if:
          - ANY test type is missing (need unit, functional, AND integration)
          - ANY test type has < 3 test functions (insufficient coverage)
          - Tests exist but have failures/errors that need fixing
          - Tests are placeholders (assert True) or trivial
          - Import errors prevent execution
          
        - **FINISH** if:
          - ALL THREE test types exist with real tests
          - Each type has 3+ test functions
          - Tests execute successfully with 0 failures
          - No import or syntax errors
          - Tests validate real functionality (not placeholders)
        
        **Your Reason Must Include**:
        - Specific assessment of EACH test type (unit, functional, integration)
        - Which test types need improvement and why
        - Concrete actions needed (e.g., "Add 2 more unit tests for error handling")
        - Clear verdict: PASS (finish) or NEEDS WORK (supervisor)
        
        **Be SPECIFIC**: Don't just say "tests need improvement" - say WHICH type 
        and WHAT specifically needs to be added or fixed.
        
        **CRITICAL - Import Errors**:
        If tests have import errors, you MUST analyze the root cause:
        - Missing sys.path configuration? → Suggest adding path to source code
        - Wrong module name? → Suggest correct import statement
        - Missing dependencies? → List what needs to be installed
        - Source code doesn't exist? → Request that code be created first
        
        Provide SPECIFIC fixes in your reason, like:
        "Unit tests fail with 'ModuleNotFoundError: No module named X'. 
        Need to add: sys.path.insert(0, '/path/to/source') at top of test files."
        '''
    
    def analyze_import_errors(self, output: str) -> dict:
        """
        Analyze pytest output for import errors and provide specific fixes
        
        Args:
            output: pytest stdout/stderr output
            
        Returns:
            Dictionary with import error analysis
        """
        import_analysis = {
            'has_import_errors': False,
            'missing_modules': [],
            'error_details': [],
            'suggested_fixes': []
        }
        
        # Pattern to match ModuleNotFoundError and ImportError
        module_error_pattern = r"ModuleNotFoundError: No module named '([^']+)'"
        import_error_pattern = r"ImportError: (.+)"
        file_pattern = r"ERROR collecting (.+\.py)"
        
        # Find all import errors
        module_errors = re.findall(module_error_pattern, output)
        import_errors = re.findall(import_error_pattern, output)
        error_files = re.findall(file_pattern, output)
        
        if module_errors or import_errors:
            import_analysis['has_import_errors'] = True
            
            # Track unique missing modules
            import_analysis['missing_modules'] = list(set(module_errors))
            
            # Provide detailed error info
            for module in import_analysis['missing_modules']:
                import_analysis['error_details'].append(
                    f"Module '{module}' not found - tests cannot import this module"
                )
            
            # Analyze and suggest fixes
            if import_analysis['missing_modules']:
                # Check if these look like local modules (not stdlib or common packages)
                local_modules = [m for m in import_analysis['missing_modules'] 
                                if not m.startswith(('sys', 'os', 'json', 'typing', 'pathlib'))]
                
                if local_modules:
                    import_analysis['suggested_fixes'].append({
                        'issue': f"Tests cannot import local modules: {', '.join(local_modules)}",
                        'fix': "Add sys.path configuration to test files",
                        'code': """import sys
from pathlib import Path
sys.path.insert(0, str(Path('/path/to/source/code')))""",
                        'action': 'Add path configuration at the top of each test file'
                    })
                    
                    import_analysis['suggested_fixes'].append({
                        'issue': "Source code path unknown",
                        'fix': "Ask supervisor for source code location",
                        'action': 'Supervisor must provide the actual path to the source code being tested'
                    })
                
                # Check for potential package naming issues
                if any('_' in m or '-' in m for m in local_modules):
                    import_analysis['suggested_fixes'].append({
                        'issue': "Module names contain special characters",
                        'fix': "Verify correct module names",
                        'action': 'Test agents may be using wrong module names - check actual file names in source'
                    })
        
        return import_analysis
    
    def verify_tests(self) -> dict:
        """
        Actually verify that tests exist and work, with per-type analysis
        
        Returns:
            Dictionary with verification results including per-type breakdown
        """
        verification = {
            'files_found': [],
            'files_missing': [],
            'execution_success': False,
            'tests_passed': 0,
            'tests_failed': 0,
            'tests_total': 0,
            'errors': [],
            'output': '',
            'by_type': {
                'unit': {'files': [], 'passed': 0, 'failed': 0, 'total': 0, 'exists': False},
                'functional': {'files': [], 'passed': 0, 'failed': 0, 'total': 0, 'exists': False},
                'integration': {'files': [], 'passed': 0, 'failed': 0, 'total': 0, 'exists': False}
            }
        }
        
        # Check which test files exist and categorize by type
        test_dirs = {
            'unit': 'unit_tests',
            'functional': 'functional_tests',
            'integration': 'integration_tests'
        }
        
        for test_type, test_dir in test_dirs.items():
            dir_path = self.output_dir / test_dir
            if dir_path.exists():
                test_files = list(dir_path.glob('test_*.py'))
                if test_files:
                    verification['by_type'][test_type]['exists'] = True
                    for f in test_files:
                        rel_path = str(f.relative_to(self.output_dir))
                        verification['files_found'].append(rel_path)
                        verification['by_type'][test_type]['files'].append(rel_path)
        
        if not verification['files_found']:
            verification['errors'].append("No test files found")
            return verification
        
        # Try to run pytest on each test type separately
        for test_type, test_dir in test_dirs.items():
            dir_path = self.output_dir / test_dir
            if not verification['by_type'][test_type]['exists']:
                continue
                
            try:
                result = subprocess.run(
                    ['pytest', str(dir_path), '-v', '--tb=short'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                # Parse output for this test type
                for line in result.stdout.split('\n'):
                    if 'passed' in line or 'failed' in line:
                        if 'passed' in line:
                            parts = line.split()
                            for i, part in enumerate(parts):
                                if 'passed' in part and i > 0:
                                    try:
                                        verification['by_type'][test_type]['passed'] = int(parts[i-1])
                                    except:
                                        pass
                        if 'failed' in line:
                            parts = line.split()
                            for i, part in enumerate(parts):
                                if 'failed' in part and i > 0:
                                    try:
                                        verification['by_type'][test_type]['failed'] = int(parts[i-1])
                                    except:
                                        pass
                
                verification['by_type'][test_type]['total'] = (
                    verification['by_type'][test_type]['passed'] + 
                    verification['by_type'][test_type]['failed']
                )
                
            except Exception as e:
                verification['errors'].append(f"{test_type} tests error: {str(e)}")
        
        # Run all tests together for overall results
        try:
            result = subprocess.run(
                ['pytest', str(self.output_dir), '-v', '--tb=short'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            verification['output'] = result.stdout + result.stderr
            verification['execution_success'] = result.returncode == 0
            
            # Analyze import errors
            import_analysis = self.analyze_import_errors(verification['output'])
            verification['import_analysis'] = import_analysis
            
            if import_analysis['has_import_errors']:
                verification['errors'].extend(import_analysis['error_details'])
            
            # Parse pytest output to count tests
            for line in result.stdout.split('\n'):
                if 'passed' in line or 'failed' in line:
                    if 'passed' in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if 'passed' in part and i > 0:
                                try:
                                    verification['tests_passed'] = int(parts[i-1])
                                except:
                                    pass
                    if 'failed' in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if 'failed' in part and i > 0:
                                try:
                                    verification['tests_failed'] = int(parts[i-1])
                                except:
                                    pass
            
            verification['tests_total'] = verification['tests_passed'] + verification['tests_failed']
            
        except subprocess.TimeoutExpired:
            verification['errors'].append("Test execution timed out")
        except FileNotFoundError:
            verification['errors'].append("pytest not found - cannot verify tests")
        except Exception as e:
            verification['errors'].append(f"Error running tests: {str(e)}")
        
        return verification
    
    def process(self, state: MessagesState) -> Command[Literal["supervisor", "__end__"]]:
        """
        Validate tests by actually running them
        
        Args:
            state: The current message state
            
        Returns:
            Command with validation decision and routing
        """
        user_question = state["messages"][0].content
        agent_answer = state["messages"][-1].content
        
        # ACTUALLY verify the tests
        print("\n🔍 Running REAL test verification...")
        verification = self.verify_tests()
        
        print(f"   Files found: {len(verification['files_found'])}")
        for f in verification['files_found']:
            print(f"     - {f}")
        
        if verification['execution_success']:
            print(f"   ✅ Tests executed successfully")
            print(f"   Tests: {verification['tests_passed']} passed, {verification['tests_failed']} failed")
        else:
            print(f"   ❌ Test execution had issues")
            if verification['errors']:
                for error in verification['errors']:
                    print(f"      Error: {error}")
        
        # Store verification in state for report agent
        state['verification_details'] = verification
        
        # Create verification summary for LLM with per-type breakdown
        type_summaries = []
        for test_type, data in verification['by_type'].items():
            status = '✅' if data['exists'] and data['failed'] == 0 and data['total'] > 0 else '❌' if data['exists'] else '⚠️'
            type_summaries.append(
                f"{status} {test_type.upper()}: {data['total']} tests "
                f"({data['passed']} passed, {data['failed']} failed) - "
                f"{len(data['files'])} files"
            )
        
        # Add import error analysis to summary if present
        import_error_section = ""
        if 'import_analysis' in verification and verification['import_analysis']['has_import_errors']:
            import_info = verification['import_analysis']
            import_error_section = f"""

⚠️ IMPORT ERRORS DETECTED:
========================
Missing Modules: {', '.join(import_info['missing_modules'])}

SUGGESTED FIXES:
"""
            for fix in import_info['suggested_fixes']:
                import_error_section += f"""
Issue: {fix['issue']}
Fix: {fix['fix']}
Action: {fix['action']}
"""
                if 'code' in fix:
                    import_error_section += f"Code to add:\n{fix['code']}\n"
        
        verification_summary = f"""
VERIFICATION RESULTS:
===================

Overall Status: {'✅ SUCCESS' if verification['execution_success'] else '❌ FAILED'}
Total: {verification['tests_total']} tests ({verification['tests_passed']} passed, {verification['tests_failed']} failed)

BY TEST TYPE:
{chr(10).join(type_summaries)}

FILES FOUND: {len(verification['files_found'])}
{chr(10).join(['  - ' + f for f in verification['files_found']])}

ERRORS: {len(verification['errors'])}
{chr(10).join(['  - ' + e for e in verification['errors']])}
{import_error_section}

Pytest Output (last 500 chars):
{verification['output'][-500:] if verification['output'] else 'No output'}

ANALYSIS REQUIRED:
- Assess if each test type (unit, functional, integration) has sufficient coverage
- Identify which test types need improvement
- Consider if any test type is missing entirely
- Evaluate test quality based on pass/fail ratios
- If import errors exist, you MUST report back to supervisor with specific fixes needed
"""

        # AUTOMATIC ROUTING: If tests cannot execute due to import errors, route to supervisor
        has_import_errors = verification.get('import_analysis', {}).get('has_import_errors', False)
        tests_collected = verification.get('tests_total', 0)
        
        if has_import_errors and tests_collected == 0:
            # Tests cannot execute - must fix before LLM evaluation
            goto = "supervisor"
            reason = f"""TESTS CANNOT EXECUTE - Import errors preventing test collection.

{import_error_section}

REQUIRED FIXES:
The test files need to be fixed before they can run. Route to the appropriate test agent(s) to:
{chr(10).join(['  - ' + fix['action'] for fix in verification['import_analysis']['suggested_fixes']])}

Verification details:
- Files found: {len(verification['files_found'])}
- Tests collected: {tests_collected}
- Errors: {len(verification['errors'])}
"""
            print("--- Workflow Transition: Validator → Supervisor (Import errors need fixing) ---")
        else:
            # Tests can execute (even if some fail) - let LLM evaluate quality
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_question},
                {"role": "assistant", "content": f"Agent Claims:\n{agent_answer}\n\n{verification_summary}"},
            ]

            response = self.llm.with_structured_output(ValidatorDecision).invoke(messages)

            goto = response.next
            reason = f"VERIFIED RESULTS: {verification['tests_passed']}/{verification['tests_total']} tests passing. {response.reason}"

            if goto == "FINISH":
                goto = "__end__"
                print("--- Workflow Transition: Validator → END ---")
            else:
                print(f"--- Workflow Transition: Validator → Supervisor ---")

        return Command(
            update={
                "messages": [
                    HumanMessage(content=reason, name="validator")
                ]
            },
            goto=goto,
        )

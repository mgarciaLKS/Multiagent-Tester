"""
Report Agent Module
Generates comprehensive reports about test generation, validation results, and coverage
"""
from typing import Literal, Dict, Any
import subprocess
from pathlib import Path
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import MessagesState

from .base_agent import BaseAgent


class ReportAgent(BaseAgent):
    """Agent that generates comprehensive test reports with coverage analysis"""
    
    def __init__(self, llm: ChatOpenAI, output_dir: Path):
        """
        Initialize the report agent
        
        Args:
            llm: The ChatOpenAI language model instance
            output_dir: Directory where test files are located
        """
        super().__init__(llm)
        self.output_dir = output_dir
        self.system_prompt = '''
        You are a professional test report generator creating stakeholder-ready documentation.
        
        **Report Structure** (MUST follow this order):
        
        1. **📊 Test Suite Status Dashboard** (ASCII diagram):
           Create a visual status board showing:
           ```
           ╔══════════════════════════════════════════════════════════╗
           ║              TEST SUITE STATUS DASHBOARD                 ║
           ╠══════════════════════════════════════════════════════════╣
           ║  Overall Status: [✅ PASS / ⚠️ NEEDS WORK / ❌ FAIL]    ║
           ║  Total Tests: XX                                         ║
           ║  Passed: XX | Failed: XX | Coverage: XX%                 ║
           ╚══════════════════════════════════════════════════════════╝
           
           ┌─────────────────────┬──────────┬──────────┬──────────┐
           │ Test Type           │ Status   │ Tests    │ Quality  │
           ├─────────────────────┼──────────┼──────────┼──────────┤
           │ 🔹 Unit Tests       │ ✅/❌    │ XX/XX    │ ⭐⭐⭐  │
           │ 🔹 Functional Tests │ ✅/❌    │ XX/XX    │ ⭐⭐⭐  │
           │ 🔹 Integration Tests│ ✅/❌    │ XX/XX    │ ⭐⭐⭐  │
           └─────────────────────┴──────────┴──────────┴──────────┘
           ```
        
        2. **📋 Executive Summary**:
           - Overall verdict (Pass/Needs Work/Fail)
           - Key achievements
           - Critical issues (if any)
           - Recommendation: Ready to merge? Or needs fixes?
        
        3. **🎯 Test Type Breakdown** (one subsection per type):
           
           ### Unit Tests
           - **Status**: ✅ Passed / ⚠️ Needs Work / ❌ Failed / ⛔ Missing
           - **Files**: List files with line counts
           - **Tests**: X passed, Y failed out of Z total
           - **Quality**: Describe what's tested and what's missing
           - **Issues**: Specific problems if any
           - **Recommendations**: What needs to be added/fixed
           
           ### Functional Tests
           (same structure)
           
           ### Integration Tests
           (same structure)
        
        4. **📈 Validation Results**:
           - What the validator found when running tests
           - Execution success/failure
           - Import errors, syntax errors
           - Validator's decision and detailed reasoning
           - Per-type validation status
        
        5. **💡 Detailed Recommendations**:
           Create a prioritized action list:
           ```
           🔴 CRITICAL (Must Fix):
           - [ ] Specific action item with context
           
           🟡 IMPORTANT (Should Fix):
           - [ ] Specific action item
           
           🟢 NICE TO HAVE (Optional):
           - [ ] Specific action item
           ```
        
        6. **📊 Coverage Analysis** (if available):
           - Overall coverage percentage
           - Coverage by module/file
           - Uncovered critical paths
        
        **Visual Guidelines**:
        - Use emojis for status (✅ ❌ ⚠️ ⭐)
        - Use ASCII tables and boxes for structure
        - Use color indicators (🔴🟡🟢) for priority
        - Use checkboxes for action items
        - Keep it professional but visually engaging
        
        **Be SPECIFIC and ACTIONABLE**:
        - Don't say "tests need improvement" - say "Add 3 unit tests for error handling in module X"
        - Don't say "some failures" - say "2 tests failed due to import error in line 5"
        - Provide file names, line numbers, specific functions to test
        '''
    
    def gather_coverage_data(self) -> Dict[str, Any]:
        """
        Run pytest with coverage to get actual coverage metrics
        
        Returns:
            Dictionary with coverage data
        """
        coverage_data = {
            'coverage_available': False,
            'overall_coverage': 0,
            'files_covered': [],
            'coverage_report': ''
        }
        
        # Check if test files exist
        test_dirs = ['unit_tests', 'functional_tests', 'integration_tests']
        test_files = []
        for test_dir in test_dirs:
            dir_path = self.output_dir / test_dir
            if dir_path.exists():
                test_files.extend(list(dir_path.glob('test_*.py')))
        
        if not test_files:
            coverage_data['coverage_report'] = "No test files found for coverage analysis"
            return coverage_data
        
        try:
            # Run pytest with coverage
            result = subprocess.run(
                ['pytest', str(self.output_dir), '--cov', '--cov-report=term', '-v'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            coverage_data['coverage_available'] = True
            coverage_data['coverage_report'] = result.stdout + result.stderr
            
            # Parse coverage percentage
            for line in result.stdout.split('\n'):
                if 'TOTAL' in line and '%' in line:
                    parts = line.split()
                    for part in parts:
                        if '%' in part:
                            try:
                                coverage_data['overall_coverage'] = int(part.replace('%', ''))
                            except:
                                pass
            
        except subprocess.TimeoutExpired:
            coverage_data['coverage_report'] = "Coverage analysis timed out"
        except FileNotFoundError:
            coverage_data['coverage_report'] = "pytest-cov not installed. Run: pip install pytest-cov"
        except Exception as e:
            coverage_data['coverage_report'] = f"Error running coverage: {str(e)}"
        
        return coverage_data
    
    def gather_test_files_info(self) -> Dict[str, Any]:
        """
        Gather information about generated test files
        
        Returns:
            Dictionary with file information
        """
        files_info = {
            'unit_tests': [],
            'functional_tests': [],
            'integration_tests': [],
            'total_files': 0,
            'total_size': 0
        }
        
        test_dirs = {
            'unit_tests': self.output_dir / 'unit_tests',
            'functional_tests': self.output_dir / 'functional_tests',
            'integration_tests': self.output_dir / 'integration_tests'
        }
        
        for test_type, dir_path in test_dirs.items():
            if dir_path.exists():
                test_files = list(dir_path.glob('*.py'))
                for f in test_files:
                    size = f.stat().st_size
                    files_info[test_type].append({
                        'name': f.name,
                        'size': size,
                        'path': str(f.relative_to(self.output_dir))
                    })
                    files_info['total_size'] += size
                files_info['total_files'] += len(test_files)
        
        return files_info
    
    def process(self, state: MessagesState) -> Command[Literal["__end__"]]:
        """
        Generate comprehensive test report
        
        Args:
            state: The current message state with all agent outputs
            
        Returns:
            Command with report
        """
        print()
        print("=" * 80)
        print("📊 GENERATING COMPREHENSIVE REPORT")
        print("=" * 80)
        print()
        
        # Gather all data
        print("📁 Gathering test file information...")
        files_info = self.gather_test_files_info()
        
        print("📊 Running coverage analysis...")
        coverage_data = self.gather_coverage_data()
        
        print("📝 Compiling report...")
        
        # Extract information from conversation history
        messages = state.get("messages", [])
        
        # Get verification details from state (set by validator)
        verification_details = state.get("verification_details", {})
        
        # Prepare context for LLM
        agent_outputs = []
        validator_info = None
        
        for msg in messages:
            content = msg.content if hasattr(msg, 'content') else str(msg)
            name = msg.name if hasattr(msg, 'name') else 'unknown'
            
            if name in ['unit_tester', 'functional_tester', 'integration_tester']:
                agent_outputs.append(f"{name}: {content[:300]}...")
            elif name == 'validator':
                validator_info = content
        
        # Build per-type status
        type_status = {}
        if verification_details and 'by_type' in verification_details:
            for test_type, data in verification_details['by_type'].items():
                status_emoji = '✅' if data['exists'] and data['failed'] == 0 and data['total'] > 0 else \
                              '⚠️' if data['exists'] and (data['failed'] > 0 or data['total'] == 0) else \
                              '❌'
                type_status[test_type] = {
                    'emoji': status_emoji,
                    'files': len(data['files']),
                    'total': data['total'],
                    'passed': data['passed'],
                    'failed': data['failed'],
                    'exists': data['exists']
                }
        
        # Create comprehensive context for report generation
        report_context = f"""
GENERATE A COMPREHENSIVE TEST GENERATION REPORT WITH VISUAL DIAGRAMS

Session Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

TEST FILES GENERATED:
====================
Total Files: {files_info['total_files']}
Total Size: {files_info['total_size']:,} bytes

Unit Tests: {len(files_info['unit_tests'])} files
{chr(10).join([f"  - {f['name']} ({f['size']:,} bytes)" for f in files_info['unit_tests']])}

Functional Tests: {len(files_info['functional_tests'])} files
{chr(10).join([f"  - {f['name']} ({f['size']:,} bytes)" for f in files_info['functional_tests']])}

Integration Tests: {len(files_info['integration_tests'])} files
{chr(10).join([f"  - {f['name']} ({f['size']:,} bytes)" for f in files_info['integration_tests']])}

PER-TYPE VERIFICATION RESULTS:
==============================
{chr(10).join([
    f"{test_type.upper()}: {data['emoji']} | Files: {data['files']} | Tests: {data['passed']}/{data['total']} passed | Failed: {data['failed']}"
    for test_type, data in type_status.items()
]) if type_status else 'No verification data available'}

AGENT OUTPUTS:
=============
{chr(10).join(agent_outputs)}

VALIDATOR ASSESSMENT:
====================
{validator_info if validator_info else "No validation information available"}

COVERAGE ANALYSIS:
=================
Coverage Available: {coverage_data['coverage_available']}
Overall Coverage: {coverage_data['overall_coverage']}%

Coverage Report:
{coverage_data['coverage_report'][-1000:] if coverage_data['coverage_report'] else 'N/A'}

INSTRUCTIONS:
============
1. Create a STATUS DASHBOARD at the top with ASCII art showing overall status
2. Break down EACH test type (unit, functional, integration) with specific status
3. For EACH type that needs work, specify EXACTLY what needs to be added/fixed
4. Use visual indicators (✅❌⚠️) and ASCII tables
5. Create a prioritized action list with checkboxes
6. Be SPECIFIC: file names, function names, number of tests needed

Generate the comprehensive markdown report following the template structure.
"""

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": report_context},
        ]

        print("🤖 Generating report with AI...")
        response = self.llm.invoke(messages)
        report_content = response.content
        
        # Save report to file
        report_file = self.output_dir / "TEST_REPORT.md"
        report_file.write_text(report_content)
        
        print(f"✅ Report saved to: {report_file}")
        print()
        print("=" * 80)
        print("📊 REPORT PREVIEW")
        print("=" * 80)
        print()
        print(report_content[:800])
        if len(report_content) > 800:
            print("\n... (see full report in TEST_REPORT.md)")
        print()
        print("=" * 80)
        
        return Command(
            update={
                "messages": [
                    HumanMessage(content=f"Report generated and saved to {report_file}", name="report_agent")
                ]
            },
            goto="__end__",
        )

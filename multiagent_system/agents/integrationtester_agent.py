"""
Integration Tester Agent Module
Handles integration testing of the application components
"""
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_experimental.tools import PythonREPLTool
from langgraph.types import Command
from langgraph.graph import MessagesState
from langgraph.prebuilt import create_react_agent

from .base_agent import BaseAgent


class IntegrationTesterAgent(BaseAgent):
    """Agent that handles integration testing of the application components"""

    def __init__(self, llm: ChatOpenAI):
        """
        Initialize the integration tester agent

        Args:
            llm: The ChatOpenAI language model instance
        """
        super().__init__(llm)
        self.python_repl_tool = PythonREPLTool()
        self.system_prompt = (
            "You are an expert integration test generator. Your mission is to CREATE COMPLETE, RUNNABLE integration test files for component interactions.\n\n"
            
            "**CRITICAL: You MUST generate actual Python test files with REAL test code, NOT placeholders or stubs!**\n\n"
            
            "**When Given a Project to Test**:\n"
            "1. **Identify Integration Points**: Find where components interact:\n"
            "   - API endpoints and their handlers\n"
            "   - Database operations (queries, transactions)\n"
            "   - External service calls (APIs, messaging)\n"
            "   - File I/O operations\n"
            "   - Inter-module communication\n"
            "2. **Analyze Dependencies**: Understand what external resources are used\n"
            "3. **Design Integration Tests**: Create tests that:\n"
            "   - Verify components work together correctly\n"
            "   - Test with real or realistic dependencies\n"
            "   - Validate data flow between components\n"
            "   - Check error handling across boundaries\n"
            "4. **WRITE COMPLETE TEST FILES**: Create actual pytest files with REAL test functions, NOT 'assert True' placeholders\n"
            "5. **Save Files**: Write files to the specified integration_tests/ directory\n"
            "6. **Report**: List the exact files created with summary of integration points tested\n\n"
            
            "**Integration Test Patterns** (YOU MUST IMPLEMENT THESE):\n"
            "- **API Testing**: Test HTTP endpoints with requests library\n"
            "- **Database Testing**: Mock database but test queries and data flow\n"
            "- **Service Integration**: Mock external APIs but test your integration layer\n"
            "- **File Operations**: Test with temporary files using pytest tmp_path\n"
            "- **Error Propagation**: Test how errors flow between components\n"
            "- **Component Communication**: Test how modules call each other\n\n"
            
            "**Example Integration Test** (THIS IS WHAT YOU MUST CREATE):\n"
            "```python\n"
            "import pytest\n"
            "from unittest.mock import Mock, patch, MagicMock, call\n"
            "from pathlib import Path\n\n"
            "def test_send_audio_message_integrates_components():\n"
            "    '''Test that audio conversion integrates with message sending'''\n"
            "    with patch('module.convert_audio') as mock_convert, \\\n"
            "         patch('module.send_file') as mock_send:\n"
            "        \n"
            "        # Setup mocks with realistic return values\n"
            "        mock_convert.return_value = Path('/tmp/audio.ogg')\n"
            "        mock_send.return_value = {'success': True, 'message_id': 'msg123'}\n"
            "        \n"
            "        # Test the integration\n"
            "        result = send_audio_message('1234567890', '/path/to/audio.mp3')\n"
            "        \n"
            "        # Verify component interaction\n"
            "        mock_convert.assert_called_once_with('/path/to/audio.mp3')\n"
            "        mock_send.assert_called_once_with('1234567890', Path('/tmp/audio.ogg'))\n"
            "        assert result['success'] == True\n"
            "        assert result['message_id'] == 'msg123'\n\n"
            "def test_error_propagation_between_components():\n"
            "    '''Test that errors from one component are handled by another'''\n"
            "    with patch('module.convert_audio') as mock_convert:\n"
            "        # Simulate error in first component\n"
            "        mock_convert.side_effect = ValueError('Invalid audio format')\n"
            "        \n"
            "        # Verify error is properly handled\n"
            "        with pytest.raises(ValueError, match='Invalid audio format'):\n"
            "            send_audio_message('1234567890', '/path/to/bad.txt')\n"
            "```\n\n"
            
            "**MANDATORY REQUIREMENTS**:\n"
            "- NO placeholders like 'assert True' or '# TODO' - write COMPLETE tests\n"
            "- Use proper mocking with unittest.mock for external dependencies\n"
            "- Include pytest imports and fixtures where needed\n"
            "- Write multiple test functions covering different integration points\n"
            "- Add docstrings explaining what integration is being tested\n"
            "- Test BOTH success paths AND error handling\n"
            "- Verify that components are called correctly (use assert_called_with)\n"
            "- Test data flow between components\n"
            "- Make tests RUNNABLE - they should execute with pytest\n\n"
            
            "**Your Response Must**:\n"
            "1. State which file(s) you are creating\n"
            "2. Provide the COMPLETE file content (imports, fixtures, multiple test functions)\n"
            "3. Confirm you saved the file(s) to the specified directory\n"
            "4. List what integration points are tested\n\n"
            
            "**Test Organization**:\n"
            "- Create comprehensive test files with 5-10 test functions minimum\n"
            "- Group related tests together\n"
            "- Use fixtures for shared setup\n"
            "- Test both success and failure scenarios\n"
            "- Validate data transformations at boundaries\n\n"
            
            "**CRITICAL - Handling Import Issues**:\n"
            "If the supervisor tells you to fix import errors in existing tests:\n"
            "1. Read the test file that has import issues\n"
            "2. Add sys.path configuration at the TOP:\n"
            "   ```python\n"
            "   import sys\n"
            "   from pathlib import Path\n"
            "   sys.path.insert(0, str(Path('/path/to/source/code')))\n"
            "   ```\n"
            "3. Use the EXACT path provided by supervisor\n"
            "4. Add any missing imports (subprocess, requests, etc.)\n"
            "5. Fix module names to match actual source files\n"
            "6. Update mocking to use correct function paths (e.g., 'module.function' not just 'function')\n\n"
            
            "**Important**:\n"
            "- Use Python code to READ project files and WRITE test files\n"
            "- Never ask questions - investigate yourself using Python\n"
            "- Always write complete, runnable test files\n"
            "- Create directories if they don't exist\n"
            "- Provide clear summary of integration points tested\n"
            "- If fixing imports, report EXACTLY what you changed"
        )
        self.code_agent = create_react_agent(
            self.llm,
            tools=[self.python_repl_tool],
            prompt=self.system_prompt
        )
    
    def process(self, state: MessagesState) -> Command[Literal["validator"]]:
        """
        Process and execute integration tests
        
        Args:
            state: The current message state
            
        Returns:
            Command with the integration test and routing to validator
        """
        try:
            result = self.code_agent.invoke(state, config={"recursion_limit": 30})
        except Exception as e:
            print(f"⚠️ IntegrationTester error: {str(e)[:100]}")
            # Return partial result even on error
            return Command(
                update={
                    "messages": [
                        HumanMessage(content=f"Integration test generation encountered an issue: {str(e)[:200]}", name="integration_tester")
                    ]
                },
                goto="validator",
            )

        print(f"--- Workflow Transition: IntegrationTester → Validator ---")

        return Command(
            update={
                "messages": [
                    HumanMessage(content=result["messages"][-1].content, name="integration_tester")
                ]
            },
            goto="validator",
        )

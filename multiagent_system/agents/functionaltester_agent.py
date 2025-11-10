"""
Functional Tester Agent Module
Tests the application as a whole emulating user scenarios
"""
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_experimental.tools import PythonREPLTool
from langgraph.types import Command
from langgraph.graph import MessagesState
from langgraph.prebuilt import create_react_agent

from .base_agent import BaseAgent


class FunctionalTesterAgent(BaseAgent):
    """Agent that tests the application as a whole emulating user scenarios"""
    
    def __init__(self, llm: ChatOpenAI):
        """
        Initialize the functional tester agent
        
        Args:
            llm: The ChatOpenAI language model instance
        """
        super().__init__(llm)
        self.python_repl_tool = PythonREPLTool()
        self.system_prompt = (
            "You are an expert functional test generator. Your mission is to CREATE COMPLETE, RUNNABLE functional test files that validate user workflows.\n\n"
            
            "**CRITICAL: You MUST generate actual Python test files with REAL test code, NOT placeholders or stubs!**\n\n"
            
            "**When Given a Project to Test**:\n"
            "1. **Understand the Application**: Read README, main files, and understand what the application does\n"
            "2. **Identify User Workflows**: Determine the key user scenarios and features\n"
            "3. **Design Test Scenarios**: Create realistic, end-to-end test cases that:\n"
            "   - Cover complete user journeys from start to finish\n"
            "   - Test interactions between multiple components\n"
            "   - Validate expected outcomes from user perspective\n"
            "   - Include both success and failure scenarios\n"
            "4. **WRITE COMPLETE TEST FILES**: Create actual pytest files with REAL test functions, NOT 'assert True' placeholders\n"
            "5. **Save Files**: Write files to the specified functional_tests/ directory\n"
            "6. **Report**: List the exact files created with summary of tests\n\n"
            
            "**Functional Test Characteristics**:\n"
            "- Test complete features, not individual functions\n"
            "- Use realistic data and scenarios\n"
            "- Test from user's perspective (inputs → outputs)\n"
            "- May involve multiple API calls or operations in sequence\n"
            "- Validate business logic and requirements\n"
            "- Mock external dependencies but test the full workflow\n"
            "- EVERY test must have REAL assertions, NOT 'assert True'\n\n"
            
            "**Example Functional Test** (THIS IS WHAT YOU MUST CREATE):\n"
            "```python\n"
            "import pytest\n"
            "from unittest.mock import Mock, patch, MagicMock\n\n"
            "def test_user_can_send_message_workflow():\n"
            "    '''Test complete workflow of user sending a message'''\n"
            "    with patch('module.search_contacts') as mock_search, \\\n"
            "         patch('module.send_message') as mock_send, \\\n"
            "         patch('module.list_messages') as mock_list:\n"
            "        \n"
            "        # Setup mocks\n"
            "        mock_search.return_value = [{'jid': '123@s.whatsapp.net', 'name': 'John'}]\n"
            "        mock_send.return_value = {'success': True, 'message_id': 'msg123'}\n"
            "        mock_list.return_value = [{'content': 'Hello', 'timestamp': 1234567890}]\n"
            "        \n"
            "        # 1. Search for contact\n"
            "        contacts = search_contacts('John')\n"
            "        assert len(contacts) > 0\n"
            "        assert contacts[0]['name'] == 'John'\n"
            "        \n"
            "        # 2. Send message to contact\n"
            "        result = send_message(contacts[0]['jid'], 'Hello')\n"
            "        assert result['success'] == True\n"
            "        assert 'message_id' in result\n"
            "        \n"
            "        # 3. Verify message appears in chat\n"
            "        messages = list_messages(chat_jid=contacts[0]['jid'])\n"
            "        assert len(messages) > 0\n"
            "        assert messages[-1]['content'] == 'Hello'\n"
            "```\n\n"
            
            "**MANDATORY REQUIREMENTS**:\n"
            "- NO placeholders like 'assert True' or '# TODO' - write COMPLETE tests\n"
            "- Use proper mocking with unittest.mock for external dependencies\n"
            "- Include pytest imports and proper test structure\n"
            "- Write multiple test functions covering different workflows\n"
            "- Add docstrings explaining what each test validates\n"
            "- Use realistic mock data and scenarios\n"
            "- Test both happy paths AND error scenarios\n"
            "- Make tests RUNNABLE - they should execute with pytest\n\n"
            
            "**Your Response Must**:\n"
            "1. State which file(s) you are creating\n"
            "2. Provide the COMPLETE file content (imports, fixtures, tests)\n"
            "3. Confirm you saved the file(s) to the specified directory\n"
            "4. List what workflows are tested\n\n"
            
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
            "6. Update mocking to use correct function paths\n\n"
            
            "**Important**:\n"
            "- Use Python code to READ project files and WRITE test files\n"
            "- Never ask questions - investigate yourself using Python\n"
            "- Always write complete, runnable test files\n"
            "- Create directories if they don't exist\n"
            "- Provide clear summary of workflows tested\n"
            "- If fixing imports, report EXACTLY what you changed"
        )
        self.code_agent = create_react_agent(
            self.llm,
            tools=[self.python_repl_tool],
            prompt=self.system_prompt
        )
    
    def process(self, state: MessagesState) -> Command[Literal["validator"]]:
        """
        Process and test the application as a whole emulating user scenarios
        
        Args:
            state: The current message state
            
        Returns:
            Command with test results and routing to validator
        """
        try:
            result = self.code_agent.invoke(state, config={"recursion_limit": 30})
        except Exception as e:
            print(f"⚠️ FunctionalTester error: {str(e)[:100]}")
            # Return partial result even on error
            return Command(
                update={
                    "messages": [
                        HumanMessage(content=f"Functional test generation encountered an issue: {str(e)[:200]}", name="functional_tester")
                    ]
                },
                goto="validator",
            )

        print(f"--- Workflow Transition: FunctionalTester → Validator ---")

        return Command(
            update={
                "messages": [
                    HumanMessage(content=result["messages"][-1].content, name="functional_tester")
                ]
            },
            goto="validator",
        )

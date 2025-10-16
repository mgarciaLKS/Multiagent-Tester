"""
Unit Tester Agent Module
Handles testing of individual components
"""
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_experimental.tools import PythonREPLTool
from langgraph.types import Command
from langgraph.graph import MessagesState
from langgraph.prebuilt import create_react_agent

from .base_agent import BaseAgent


class UnitTesterAgent(BaseAgent):
    """Agent that handles unit testing of individual components"""
    
    def __init__(self, llm: ChatOpenAI):
        """
        Initialize the unit tester agent

        Args:
            llm: The ChatOpenAI language model instance
        """
        super().__init__(llm)
        self.python_repl_tool = PythonREPLTool()
        self.code_agent = create_react_agent(
            llm,
            tools=[self.python_repl_tool],
            prompt=(
                "You are an expert unit test generator. Your mission is to create comprehensive, high-quality unit tests for Python code.\n\n"
                
                "**When Given a Project/File to Test**:\n"
                "1. **Read & Analyze**: Use Python code to read the file(s) you're assigned to test\n"
                "2. **Identify Test Cases**: Find all functions, methods, classes that need unit tests\n"
                "3. **Generate Tests**: Create pytest unit tests with:\n"
                "   - Proper imports (pytest, unittest.mock if needed)\n"
                "   - Descriptive test names (test_function_name_expected_behavior)\n"
                "   - Arrange-Act-Assert pattern\n"
                "   - Edge cases, error cases, normal cases\n"
                "   - Mock external dependencies\n"
                "   - Fixtures for setup/teardown\n"
                "4. **Write Test File**: Save tests to 'tests/test_<module_name>.py'\n"
                "5. **Report**: Provide summary of tests created, coverage estimation, and any challenges\n\n"
                
                "**Test Quality Standards**:\n"
                "- Each function/method should have 3-5 test cases minimum\n"
                "- Use descriptive test names that explain what's being tested\n"
                "- Include docstrings in test functions\n"
                "- Test happy paths, edge cases, and error conditions\n"
                "- Mock external dependencies (APIs, databases, files)\n"
                "- Use pytest fixtures for common setup\n"
                "- Aim for 80%+ code coverage per function\n\n"
                
                "**Example Test Structure**:\n"
                "```python\n"
                "import pytest\n"
                "from unittest.mock import Mock, patch\n"
                "from mymodule import my_function\n\n"
                "def test_my_function_with_valid_input():\n"
                "    \"\"\"Test my_function handles valid input correctly\"\"\"\n"
                "    result = my_function('valid')\n"
                "    assert result == expected_value\n"
                "```\n\n"
                
                "**Important**:\n"
                "- Never ask questions - read files yourself using Python\n"
                "- Always write complete, runnable test files\n"
                "- Create tests/ directory if it doesn't exist\n"
                "- Follow pytest conventions and best practices\n"
                "- Provide clear summary of what you tested and coverage achieved"
            )
        )
    
    def process(self, state: MessagesState) -> Command[Literal["validator"]]:
        """
        Process and execute unit tests
        
        Args:
            state: The current message state
            
        Returns:
            Command with test results and routing to validator
        """
        result = self.code_agent.invoke(state)

        print(f"--- Workflow Transition: UnitTester → Validator ---")

        return Command(
            update={
                "messages": [
                    HumanMessage(content=result["messages"][-1].content, name="unit_tester")
                ]
            },
            goto="validator",
        )

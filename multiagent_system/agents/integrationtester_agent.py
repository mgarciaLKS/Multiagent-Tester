"""
Integration Tester Agent Module
Handles integration testing of the application components
"""
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import MessagesState

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
        self.system_prompt = (
            "You are an expert integration test generator. Your mission is to create tests for component interactions and external dependencies.\n\n"
            
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
            "4. **Generate Tests**: Write pytest integration tests in 'tests/integration/'\n"
            "5. **Report**: Summarize integration points tested and potential issues\n\n"
            
            "**Integration Test Patterns**:\n"
            "- **API Testing**: Test HTTP endpoints with requests library\n"
            "- **Database Testing**: Use test database or transactions with rollback\n"
            "- **Service Mocking**: Mock external APIs but test your integration code\n"
            "- **File Operations**: Test with temporary files/directories\n"
            "- **Error Propagation**: Test how errors flow between components\n\n"
            
            "**Example Integration Test**:\n"
            "```python\n"
            "import pytest\n"
            "from unittest.mock import Mock, patch\n\n"
            "def test_send_message_integrates_with_whatsapp_api():\n"
            "    '''Test that send_message properly integrates with WhatsApp API'''\n"
            "    with patch('whatsapp.api_client') as mock_client:\n"
            "        mock_client.send.return_value = {'success': True}\n"
            "        \n"
            "        result = send_message('1234567890', 'Test message')\n"
            "        \n"
            "        # Verify integration: correct API call made\n"
            "        mock_client.send.assert_called_once_with(\n"
            "            to='1234567890',\n"
            "            message='Test message'\n"
            "        )\n"
            "        assert result['success'] == True\n"
            "```\n\n"
            
            "**Test Organization**:\n"
            "- Group tests by integration type (API, database, external services)\n"
            "- Use fixtures for setup (test databases, mock servers)\n"
            "- Test both success and failure scenarios\n"
            "- Validate data transformations at boundaries\n"
            "- Check that errors are properly handled and propagated\n\n"
            
            "**Important**:\n"
            "- Focus on INTERACTIONS between components, not individual logic\n"
            "- Test real integration code, mock only external dependencies\n"
            "- Verify data correctly flows between components\n"
            "- Create tests/integration/ directory if needed\n"
            "- Provide summary of integration points covered"
        )
    
    def process(self, state: MessagesState) -> Command[Literal["validator"]]:
        """
        Process and execute integration tests
        
        Args:
            state: The current message state
            
        Returns:
            Command with the integration test and routing to validator
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
        ] + state["messages"]

        enhanced_query = self.llm.invoke(messages)

        print(f"--- Workflow Transition: IntegrationTester → Validator ---")

        return Command(
            update={
                "messages": [
                    HumanMessage(
                        content=enhanced_query.content,
                        name="integration_tester"
                    )
                ]
            },
            goto="validator",
        )

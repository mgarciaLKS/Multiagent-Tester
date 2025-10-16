"""
Functional Tester Agent Module
Tests the application as a whole emulating user scenarios
"""
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import MessagesState

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
        self.system_prompt = (
            "You are an expert functional test generator. Your mission is to create end-to-end tests that validate complete user workflows.\n\n"
            
            "**When Given a Project to Test**:\n"
            "1. **Understand the Application**: Read README, main files, and understand what the application does\n"
            "2. **Identify User Workflows**: Determine the key user scenarios and features\n"
            "3. **Design Test Scenarios**: Create realistic, end-to-end test cases that:\n"
            "   - Cover complete user journeys from start to finish\n"
            "   - Test interactions between multiple components\n"
            "   - Validate expected outcomes from user perspective\n"
            "   - Include both success and failure scenarios\n"
            "4. **Generate Tests**: Write pytest functional tests in 'tests/functional/'\n"
            "5. **Report**: Summarize scenarios tested and coverage of user workflows\n\n"
            
            "**Functional Test Characteristics**:\n"
            "- Test complete features, not individual functions\n"
            "- Use realistic data and scenarios\n"
            "- Test from user's perspective (inputs → outputs)\n"
            "- May involve multiple API calls or operations in sequence\n"
            "- Validate business logic and requirements\n"
            "- Can use integration test fixtures but focus on workflows\n\n"
            
            "**Example Functional Test**:\n"
            "```python\n"
            "def test_user_can_send_message_workflow():\n"
            "    '''Test complete workflow of user sending a message'''\n"
            "    # 1. Search for contact\n"
            "    contacts = search_contacts('John')\n"
            "    assert len(contacts) > 0\n"
            "    \n"
            "    # 2. Send message to contact\n"
            "    result = send_message(contacts[0]['jid'], 'Hello')\n"
            "    assert result['success'] == True\n"
            "    \n"
            "    # 3. Verify message appears in chat\n"
            "    messages = list_messages(chat_jid=contacts[0]['jid'])\n"
            "    assert 'Hello' in messages[-1]['content']\n"
            "```\n\n"
            
            "**Important**:\n"
            "- Focus on USER VALUE, not technical implementation\n"
            "- Test realistic scenarios users would actually do\n"
            "- Each test should tell a story of user interaction\n"
            "- Create tests/functional/ directory if needed\n"
            "- Provide summary of user workflows covered"
        )
    
    def process(self, state: MessagesState) -> Command[Literal["validator"]]:
        """
        Process and test the application as a whole emulating user scenarios
        
        Args:
            state: The current message state
            
        Returns:
            Command with test results and routing to validator
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
        ] + state["messages"]

        enhanced_query = self.llm.invoke(messages)

        print(f"--- Workflow Transition: FunctionalTester → Validator ---")

        return Command(
            update={
                "messages": [
                    HumanMessage(
                        content=enhanced_query.content,
                        name="functional_tester"
                    )
                ]
            },
            goto="validator",
        )

"""
Validator Agent Module
Validates the quality of the tests and decides whether to continue or finish
"""
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import MessagesState

from .base_agent import BaseAgent
from ..models.decisions import ValidatorDecision


class ValidatorAgent(BaseAgent):
    """Agent that validates the quality of the tests and decides whether to continue or finish"""
    
    def __init__(self, llm: ChatOpenAI):
        """
        Initialize the validator agent
        
        Args:
            llm: The ChatOpenAI language model instance
        """
        super().__init__(llm)
        self.system_prompt = '''
        You are a test quality validator. Your role is to evaluate generated tests and decide if more testing is needed.
        
        **Evaluation Criteria**:
        
        1. **Test Coverage**:
           - Were test files actually created?
           - Do tests cover the assigned components/files?
           - Are critical paths and edge cases tested?
           - Aim for 70%+ code coverage minimum
        
        2. **Test Quality**:
           - Do tests follow pytest best practices?
           - Are test names descriptive?
           - Do tests have proper structure (Arrange-Act-Assert)?
           - Are mocks used appropriately for external dependencies?
           - Do tests have clear assertions?
        
        3. **Completeness**:
           - Did the agent complete their assigned task?
           - Are there obvious gaps in test coverage?
           - Do tests cover both success and failure scenarios?
        
        4. **Project Coverage**:
           - Which files/components have been tested so far?
           - Which critical files/components still need tests?
           - Are we approaching comprehensive coverage?
        
        **Decision Logic**:
        
        - **Route to Supervisor** if:
          - Tests were created but more files/components need testing
          - Current test type is complete but need other test types (e.g., unit tests done, need integration tests)
          - Critical components are untested
          - Test coverage is below 70% overall
        
        - **FINISH** if:
          - Comprehensive test suite exists (unit, integration, functional)
          - All critical components are tested
          - Test coverage is 70%+ with good quality
          - No obvious gaps in testing
        
        **Your Response Should Include**:
        - What was tested in this iteration
        - Quality assessment of generated tests
        - Estimated coverage so far
        - What still needs testing (if continuing)
        - Clear decision rationale
        '''
    
    def process(self, state: MessagesState) -> Command[Literal["supervisor", "__end__"]]:
        """
        Validate response tests and determine next step
        
        Args:
            state: The current message state
            
        Returns:
            Command with validation decision and routing
        """
        user_question = state["messages"][0].content
        agent_answer = state["messages"][-1].content

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_question},
            {"role": "assistant", "content": agent_answer},
        ]

        response = self.llm.with_structured_output(ValidatorDecision).invoke(messages)

        goto = response.next
        reason = response.reason

        if goto == "FINISH":
            goto = "__end__"
            print(" --- Transitioning to END ---")
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

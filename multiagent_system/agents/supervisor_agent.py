"""
Supervisor Agent Module
Orchestrates the workflow by routing to appropriate specialist agents
"""
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import MessagesState

from .base_agent import BaseAgent
from ..models.decisions import SupervisorDecision


class SupervisorAgent(BaseAgent):
    """Supervisor agent that orchestrates the workflow by routing to appropriate specialists"""
    
    def __init__(self, llm: ChatOpenAI):
        """
        Initialize the supervisor agent
        
        Args:
            llm: The ChatOpenAI language model instance
        """
        super().__init__(llm)
        self.system_prompt = '''
        You are a workflow supervisor managing a team of specialized testing agents: Unit Tester, Functional Tester and Integration Tester.
        
        Your role is to analyze projects and orchestrate comprehensive test generation by routing ALL THREE agents IN PARALLEL.

        **Team Members**:
        1. **Unit Tester**: Generates tests for individual functions, classes, and methods. Tests isolated components for correctness.
        2. **Functional Tester**: Generates end-to-end tests for user workflows and application features. Tests the application as a whole.
        3. **Integration Tester**: Generates tests for component interactions, API calls, database operations, and external dependencies.

        **CRITICAL - First Iteration Strategy**:
        On the FIRST iteration (when no tests exist yet), you MUST route to "unit_tester" BUT your message must contain:
        
        1. **Detailed Project Analysis**: Analyze the project structure from the user's request
        2. **Specific Instructions for ALL THREE test types** in your reason message:
        
        ```
        PROJECT ANALYSIS:
        - Project path: [extract from request]
        - Files to test: [list all mentioned files]
        
        INSTRUCTIONS FOR PARALLEL EXECUTION:
        
        📋 UNIT TESTS (test individual classes/functions):
        Files: [list specific .py files for unit testing]
        Focus: models.py (Task, User classes), database.py (Database class), services.py (TaskService, UserService)
        Output: unit_tests/test_models.py, test_database.py, test_services.py
        
        📋 FUNCTIONAL TESTS (test workflows):
        Files: [list files for functional testing]
        Focus: Complete user workflows using services layer (create→complete→delete task flow)
        Output: functional_tests/test_task_workflows.py, test_user_workflows.py
        
        📋 INTEGRATION TESTS (test full stack):
        Files: [list files for integration testing]
        Focus: API → Service → Database integration, end-to-end API calls
        Output: integration_tests/test_api_integration.py
        ```
        
        This way, even though you route to "unit_tester", ALL THREE agents will receive these instructions when they run in parallel.

        **Decision Guidelines**:
        - **First iteration (no tests)** → Route to "unit_tester" BUT include instructions for ALL THREE types in your reason
        - **Subsequent iterations** → Route to specific agent that needs fixes based on validator feedback
        - Always provide clear, actionable instructions with file paths and focus areas

        **CRITICAL - Handling Validator Feedback**:
        When the Validator reports issues with tests:
        
        1. **Import Errors**: If validator reports ModuleNotFoundError or import issues:
           - Identify which test agent created those tests (unit/functional/integration)
           - Route back to that SAME agent with specific instructions to fix imports
           - Include the EXACT fix needed (e.g., "Add sys.path.insert(0, '/path/to/source')")
           - Provide the source code path if known from the original request
        
        2. **Test Logic Errors**: If tests fail due to wrong mocking or assertions:
           - Route to the responsible agent with details about what failed
           - Specify what needs to be corrected (e.g., "Mock 'module.function' not 'function' directly")
        
        3. **Missing Tests**: If validator says insufficient tests (<3 per type):
           - Route to appropriate agent requesting more tests
           - Be specific: "Add 2 more unit tests for error handling in function X"
        
        **When Routing for Fixes**:
        Your reason MUST include:
        - What exactly is wrong (from validator feedback)
        - Which files need fixing
        - The specific fix or improvement needed
        - Example code if it's an import issue
        
        Example: "Unit tests have import errors for 'audio' module. Route to unit_tester to add:
        ```python
        import sys
        sys.path.insert(0, '/home/user/project/src')
        ```
        at the top of test_audio.py"

        Your main objective is to generate a comprehensive test suite that ensures code quality, reliability, and correctness.
        '''

    def process(self, state: MessagesState) -> Command[Literal["unit_tester", "functional_tester", "integration_tester"]]:
        """
        Process state and route to appropriate agent
        
        Args:
            state: The current message state
            
        Returns:
            Command with routing decision and updated state
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
        ] + state["messages"]

        response = self.llm.with_structured_output(SupervisorDecision).invoke(messages)
        
        goto = response.next
        reason = response.reason

        print(f"--- Workflow Transition: Supervisor → {goto.upper()} ---")

        return Command(
            update={
                "messages": [
                    HumanMessage(content=reason, name="supervisor")
                ]
            },
            goto=goto,
        )

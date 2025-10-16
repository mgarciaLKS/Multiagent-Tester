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
        
        Your role is to analyze projects and orchestrate comprehensive test generation by routing tasks to appropriate specialists.

        **Team Members**:
        1. **Unit Tester**: Generates tests for individual functions, classes, and methods. Tests isolated components for correctness.
        2. **Functional Tester**: Generates end-to-end tests for user workflows and application features. Tests the application as a whole.
        3. **Integration Tester**: Generates tests for component interactions, API calls, database operations, and external dependencies.

        **Your Workflow for Project Testing**:
        1. **Analyze Project Structure**: When given a project path, first understand what files exist, their purposes, and dependencies.
        2. **Prioritize Testing**: Start with unit tests (fastest to write, most coverage), then integration tests (critical paths), then functional tests (complete scenarios).
        3. **Route Strategically**: 
           - Route to Unit Tester for: individual functions, utility methods, data models, business logic
           - Route to Integration Tester for: API endpoints, database operations, external service calls, module interactions
           - Route to Functional Tester for: complete user workflows, feature scenarios, end-to-end application behavior
        4. **Build Incrementally**: Each agent should generate tests for specific files/functions, then return to you for the next assignment.
        5. **Track Progress**: Keep track of which files/components have been tested and which need tests.

        **Decision Guidelines**:
        - If no tests exist yet → Start with Unit Tester for core business logic
        - If unit tests are in progress → Continue with Unit Tester or move to Integration Tester for critical paths
        - If unit & integration tests exist → Route to Functional Tester for end-to-end scenarios
        - Always provide clear rationale: which files/functions to test and why

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

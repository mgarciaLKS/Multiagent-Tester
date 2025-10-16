"""
Agent classes for the multi-agent workflow system
"""
from abc import ABC, abstractmethod
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI
from langgraph.types import Command
from langgraph.graph import MessagesState
from langgraph.prebuilt import create_react_agent


class BaseAgent(ABC):
    """Base class for all agents in the workflow"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
    
    @abstractmethod
    def process(self, state: MessagesState) -> Command:
        """Process the current state and return a command for the next step"""
        pass


class SupervisorDecision(BaseModel):
    """Pydantic model for supervisor routing decisions"""
    next: Literal["enhancer", "researcher", "coder", "generic"] = Field(
        description="Determines which specialist to activate next in the workflow sequence: "
                    "'enhancer' when user input requires clarification, expansion, or refinement, "
                    "'researcher' when additional facts, context, or data collection is necessary, "
                    "'coder' when implementation, computation, or technical problem-solving is required."
                    "'generic' when any other question is given."
    )
    reason: str = Field(
        description="Detailed justification for the routing decision, explaining the rationale behind selecting the particular specialist and how this advances the task toward completion."
    )


class SupervisorAgent(BaseAgent):
    """Supervisor agent that orchestrates the workflow by routing to appropriate specialists"""
    
    def __init__(self, llm: ChatOpenAI):
        super().__init__(llm)
        self.system_prompt = '''
        You are a workflow supervisor managing a team of three specialized agents: Prompt Enhancer, Researcher, and Coder. Your role is to orchestrate the workflow by selecting the most appropriate next agent based on the current state and needs of the task. Provide a clear, concise rationale for each decision to ensure transparency in your decision-making process.

        **Team Members**:
        1. **Prompt Enhancer**: Always consider this agent first. They clarify ambiguous requests, improve poorly defined queries, and ensure the task is well-structured before deeper processing begins.
        2. **Researcher**: Specializes in information gathering, fact-finding, and collecting relevant data needed to address the user's request.
        3. **Coder**: Focuses on technical implementation, calculations, data analysis, algorithm development, and coding solutions.
        4. **Generic**: if the question is a generic topic that can be answered without calling researcher or coder, just use this agent

        **Your Responsibilities**:
        1. Analyze each user request and agent response for completeness, accuracy, and relevance.
        2. Route the task to the most appropriate agent at each decision point.
        3. Maintain workflow momentum by avoiding redundant agent assignments.
        4. Continue the process until the user's request is fully and satisfactorily resolved.

        Your objective is to create an efficient workflow that leverages each agent's strengths while minimizing unnecessary steps, ultimately delivering complete and accurate solutions to user requests.
        '''
    
    def process(self, state: MessagesState) -> Command[Literal["enhancer", "researcher", "coder", "generic"]]:
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


class EnhancerAgent(BaseAgent):
    """Agent that improves and clarifies user queries"""
    
    def __init__(self, llm: ChatOpenAI):
        super().__init__(llm)
        self.system_prompt = (
            "You are a Query Refinement Specialist with expertise in transforming vague requests into precise instructions. Your responsibilities include:\n\n"
            "1. Analyzing the original query to identify key intent and requirements\n"
            "2. Resolving any ambiguities without requesting additional user input\n"
            "3. Expanding underdeveloped aspects of the query with reasonable assumptions\n"
            "4. Restructuring the query for clarity and actionability\n"
            "5. Ensuring all technical terminology is properly defined in context\n\n"
            "Important: Never ask questions back to the user. Instead, make informed assumptions and create the most comprehensive version of their request possible."
        )
    
    def process(self, state: MessagesState) -> Command[Literal["supervisor"]]:
        messages = [
            {"role": "system", "content": self.system_prompt},
        ] + state["messages"]

        enhanced_query = self.llm.invoke(messages)

        print(f"--- Workflow Transition: Prompt Enhancer → Supervisor ---")

        return Command(
            update={
                "messages": [
                    HumanMessage(
                        content=enhanced_query.content,
                        name="enhancer"
                    )
                ]
            },
            goto="supervisor",
        )


class ResearcherAgent(BaseAgent):
    """Agent that gathers information using web search"""
    
    def __init__(self, llm: ChatOpenAI):
        super().__init__(llm)
        self.tavily_search = TavilySearchResults(max_results=2)
        self.research_agent = create_react_agent(
            llm,
            tools=[self.tavily_search],
            prompt=(
                "You are an Information Specialist with expertise in comprehensive research. Your responsibilities include:\n\n"
                "1. Identifying key information needs based on the query context\n"
                "2. Gathering relevant, accurate, and up-to-date information from reliable sources\n"
                "3. Organizing findings in a structured, easily digestible format\n"
                "4. Citing sources when possible to establish credibility\n"
                "5. Focusing exclusively on information gathering - avoid analysis or implementation\n\n"
                "Provide thorough, factual responses without speculation where information is unavailable."
            )
        )
    
    def process(self, state: MessagesState) -> Command[Literal["validator"]]:
        result = self.research_agent.invoke(state)

        print(f"--- Workflow Transition: Researcher → Validator ---")

        return Command(
            update={
                "messages": [
                    HumanMessage(
                        content=result["messages"][-1].content,
                        name="researcher"
                    )
                ]
            },
            goto="validator",
        )


class CoderAgent(BaseAgent):
    """Agent that handles technical implementation and calculations"""
    
    def __init__(self, llm: ChatOpenAI):
        super().__init__(llm)
        self.python_repl_tool = PythonREPLTool()
        self.code_agent = create_react_agent(
            llm,
            tools=[self.python_repl_tool],
            prompt=(
                "You are a coder and analyst. Focus on mathematical calculations, analyzing, solving math questions, "
                "and executing code. Handle technical problem-solving and data tasks."
            )
        )
    
    def process(self, state: MessagesState) -> Command[Literal["validator"]]:
        result = self.code_agent.invoke(state)

        print(f"--- Workflow Transition: Coder → Validator ---")

        return Command(
            update={
                "messages": [
                    HumanMessage(content=result["messages"][-1].content, name="coder")
                ]
            },
            goto="validator",
        )


class GenericAgent(BaseAgent):
    """Agent that handles general questions that don't require specialized processing"""
    
    def __init__(self, llm: ChatOpenAI):
        super().__init__(llm)
        self.system_prompt = "Answer the question:"
    
    def process(self, state: MessagesState) -> Command[Literal["validator"]]:
        messages = [
            {"role": "system", "content": self.system_prompt},
        ] + state["messages"]

        enhanced_query = self.llm.invoke(messages)

        print(f"--- Workflow Transition: Generic → Validator ---")

        return Command(
            update={
                "messages": [
                    HumanMessage(
                        content=enhanced_query.content,
                        name="generic"
                    )
                ]
            },
            goto="validator",
        )


class ValidatorDecision(BaseModel):
    """Pydantic model for validator decisions"""
    next: Literal["supervisor", "FINISH"] = Field(
        description="Specifies the next worker in the pipeline: 'supervisor' to continue or 'FINISH' to terminate."
    )
    reason: str = Field(
        description="The reason for the decision."
    )


class ValidatorAgent(BaseAgent):
    """Agent that validates the quality of responses and decides whether to continue or finish"""
    
    def __init__(self, llm: ChatOpenAI):
        super().__init__(llm)
        self.system_prompt = '''
        Your task is to ensure reasonable quality.
        Specifically, you must:
        - Review the user's question (the first message in the workflow).
        - Review the answer (the last message in the workflow).
        - If the answer addresses the core intent of the question, even if not perfectly, signal to end the workflow with 'FINISH'.
        - Only route back to the supervisor if the answer is completely off-topic, harmful, or fundamentally misunderstands the question.

        - Accept answers that are "good enough" rather than perfect
        - Prioritize workflow completion over perfect responses
        - Give benefit of doubt to borderline answers

        Routing Guidelines:
        1. 'supervisor' Agent: ONLY for responses that are completely incorrect or off-topic.
        2. Respond with 'FINISH' in all other cases to end the workflow.
        '''
    
    def process(self, state: MessagesState) -> Command[Literal["supervisor", "__end__"]]:
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

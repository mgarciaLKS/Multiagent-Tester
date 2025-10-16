"""
Base Agent Module
Provides the abstract base class for all agents in the workflow
"""
from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from langgraph.types import Command
from langgraph.graph import MessagesState


class BaseAgent(ABC):
    """Abstract base class for all agents in the workflow"""
    
    def __init__(self, llm: ChatOpenAI):
        """
        Initialize the agent with a language model
        
        Args:
            llm: The ChatOpenAI language model instance
        """
        self.llm = llm
    
    @abstractmethod
    def process(self, state: MessagesState) -> Command:
        """
        Process the current state and return a command for the next step
        
        Args:
            state: The current message state
            
        Returns:
            Command with updated state and routing information
        """
        pass

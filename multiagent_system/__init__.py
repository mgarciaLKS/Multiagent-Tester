"""
Multi-Agent Workflow System
A supervisor-based multi-agent system for handling various types of queries

Modular architecture with separate files for each component
"""
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import main workflow class
from .workflow import MultiAgentWorkflow

# Import all agents
from .agents import (
    BaseAgent,
    SupervisorAgent,
    FunctionalTesterAgent,
    UnitTesterAgent,
    IntegrationTesterAgent,
    ValidatorAgent,
)

# Import decision models
from .models import (
    SupervisorDecision,
    ValidatorDecision,
)

__version__ = "1.0.0"

__all__ = [
    "MultiAgentWorkflow",
    "BaseAgent",
    "SupervisorAgent",
    "FunctionalTesterAgent",
    "UnitTesterAgent",
    "IntegrationTesterAgent",
    "ValidatorAgent",
    "SupervisorDecision",
    "ValidatorDecision",
]

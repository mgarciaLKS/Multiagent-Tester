"""
Multi-Agent System Package
A modular multi-agent workflow system using LangGraph
"""

from .workflow import MultiAgentWorkflow
from .parallel_workflow import ParallelTestingWorkflow
from .agents import (
    SupervisorAgent,
    FunctionalTesterAgent,
    UnitTesterAgent,
    IntegrationTesterAgent,
    ValidatorAgent,
)
from .models.decisions import SupervisorDecision, ValidatorDecision

__version__ = "1.0.0"

__all__ = [
    "MultiAgentWorkflow",
    "ParallelTestingWorkflow",
    "SupervisorAgent",
    "FunctionalTesterAgent",
    "UnitTesterAgent",
    "IntegrationTesterAgent",
    "ValidatorAgent",
    "SupervisorDecision",
    "ValidatorDecision",
]

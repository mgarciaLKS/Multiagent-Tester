"""
Multi-Agent Testing System
Parallel execution workflow for automated test generation
"""

from .parallel_workflow import ParallelTestingWorkflow as MultiAgentWorkflow
from .agents import (
    SupervisorAgent,
    FunctionalTesterAgent,
    UnitTesterAgent,
    IntegrationTesterAgent,
    ValidatorAgent,
)
from .models.decisions import SupervisorDecision, ValidatorDecision

__version__ = "2.0.0"

__all__ = [
    "MultiAgentWorkflow",
    "SupervisorAgent",
    "FunctionalTesterAgent",
    "UnitTesterAgent",
    "IntegrationTesterAgent",
    "ValidatorAgent",
    "SupervisorDecision",
    "ValidatorDecision",
]

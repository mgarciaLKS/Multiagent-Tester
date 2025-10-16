"""
Decision Models Module
Pydantic models for structured outputs from agents
"""
from typing import Literal
from pydantic import BaseModel, Field


class SupervisorDecision(BaseModel):
    """Pydantic model for supervisor routing decisions"""
    next: Literal["unit_tester", "functional_tester", "integration_tester"] = Field(
        description="Determines which testing specialist to activate next in the workflow sequence: "
                    "'unit_tester' when individual components need to be tested for correctness, "
                    "'functional_tester' when the application as a whole needs to be tested by emulating user scenarios, "
                    "'integration_tester' when different components need to be tested together for integration."
    )
    reason: str = Field(
        description="Detailed justification for the routing decision, explaining the rationale "
                    "behind selecting the particular testing specialist and how this advances the testing toward completion."
    )


class ValidatorDecision(BaseModel):
    """Pydantic model for validator decisions"""
    next: Literal["supervisor", "FINISH"] = Field(
        description="Specifies the next worker in the pipeline: 'supervisor' to continue or 'FINISH' to terminate."
    )
    reason: str = Field(
        description="The reason for the decision."
    )

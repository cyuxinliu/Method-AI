"""Pydantic schemas for API requests and responses."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ExperienceLevel(str, Enum):
    """Experience level of the user."""

    UNDERGRAD = "undergrad"
    GRAD = "grad"
    POSTDOC = "postdoc"
    INDUSTRY = "industry"


class FeedbackOutcome(str, Enum):
    """Outcome of a procedure execution."""

    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    UNKNOWN = "unknown"


class LabContext(BaseModel):
    """Laboratory context and constraints."""

    scale_mg: float = Field(..., description="Target scale in milligrams", gt=0)
    equipment: list[str] = Field(
        default_factory=list, description="Available equipment"
    )
    purification_methods: list[str] = Field(
        default_factory=list, description="Available purification methods"
    )
    safety_constraints: list[str] = Field(
        default_factory=list, description="Safety limitations or requirements"
    )
    experience_level: ExperienceLevel = Field(
        ..., description="Experience level of the user"
    )
    time_budget_hours: float = Field(
        ..., description="Available time in hours", gt=0
    )


class ProcedureStep(BaseModel):
    """A single step in a procedure."""

    step_number: int = Field(..., description="Step order (1-indexed)", ge=1)
    action: str = Field(..., description="Action to perform")
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Step parameters"
    )
    rationale: str | None = Field(None, description="Explanation for the step")


class GenerateProcedureRequest(BaseModel):
    """Request to generate a procedure."""

    target_smiles: str = Field(..., description="Target molecule in SMILES format")
    lab_context: LabContext = Field(..., description="Laboratory constraints")
    retrosynthesis_plan: dict[str, Any] | None = Field(
        None, description="Optional pre-computed retrosynthesis plan"
    )
    notes: str | None = Field(None, description="Additional context or notes")


class GenerateProcedureResponse(BaseModel):
    """Response containing generated procedure."""

    procedure: list[ProcedureStep] = Field(..., description="Generated procedure steps")
    risk_flags: list[str] = Field(
        default_factory=list, description="Identified risk factors"
    )
    fallback_options: list[str] = Field(
        default_factory=list, description="Alternative approaches"
    )
    citations: list[str] = Field(
        default_factory=list, description="References if any"
    )
    disclaimer: str = Field(..., description="Safety disclaimer")
    version: str = Field(..., description="API version")
    request_id: str = Field(..., description="Unique request identifier")


class FeedbackRequest(BaseModel):
    """Request to submit feedback."""

    request_id: str = Field(..., description="Original request ID")
    edits: str = Field(..., description="Description of changes made")
    outcome: FeedbackOutcome = Field(..., description="Outcome of the procedure")
    notes: str | None = Field(None, description="Additional feedback notes")


class FeedbackResponse(BaseModel):
    """Response confirming feedback storage."""

    stored: bool = Field(..., description="Whether feedback was stored successfully")

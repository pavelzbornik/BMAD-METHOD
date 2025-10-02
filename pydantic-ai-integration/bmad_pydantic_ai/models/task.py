"""Pydantic models for BMAD task specifications."""

from typing import List, Optional
from pydantic import BaseModel, Field


class TaskStep(BaseModel):
    """A single step in a task workflow."""
    
    number: int
    description: str
    instruction: Optional[str] = None
    substeps: List["TaskStep"] = Field(default_factory=list)


class TaskSpec(BaseModel):
    """BMAD task specification."""
    
    id: str
    title: str
    purpose: Optional[str] = None
    
    # Elicitation flag
    elicit: bool = Field(default=False, description="Requires user interaction")
    
    # Instructions
    instructions: List[str] = Field(default_factory=list)
    steps: List[TaskStep] = Field(default_factory=list)
    
    # Usage scenarios
    scenarios: Optional[List[str]] = None
    
    # Raw content
    raw_markdown: Optional[str] = None


class ElicitationMethod(BaseModel):
    """An elicitation method option."""
    
    id: str
    name: str
    description: str
    category: Optional[str] = None
    context_types: List[str] = Field(default_factory=list)


class ElicitationSession(BaseModel):
    """State for an active elicitation session."""
    
    context: str
    content_type: str
    selected_methods: List[str] = Field(default_factory=list)
    available_methods: List[ElicitationMethod] = Field(default_factory=list)
    iteration_count: int = 0

"""Pydantic models for BMAD template specifications."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TemplateMetadata(BaseModel):
    """Template metadata."""
    
    id: str
    name: str
    version: str
    output: Dict[str, str] = Field(default_factory=dict)
    
    @classmethod
    def model_validate(cls, obj):
        """Custom validation to handle version as number."""
        if isinstance(obj, dict) and "version" in obj and not isinstance(obj["version"], str):
            obj = obj.copy()
            obj["version"] = str(obj["version"])
        return super().model_validate(obj)


class WorkflowConfig(BaseModel):
    """Workflow configuration."""
    
    mode: str = Field(default="interactive")
    elicitation: Optional[str] = None


class TemplateSection(BaseModel):
    """A section in a template."""
    
    id: str
    title: str
    type: Optional[str] = None
    instruction: Optional[str] = None
    
    # Conditional sections
    condition: Optional[str] = None
    
    # Content configuration
    prefix: Optional[str] = None
    template: Optional[str] = None
    examples: List[str] = Field(default_factory=list)
    columns: Optional[List[str]] = None
    
    # Elicitation
    elicit: bool = False
    
    # Choices for user selection
    choices: Optional[Dict[str, List[str]]] = None
    
    # Nested sections
    sections: List["TemplateSection"] = Field(default_factory=list)


class TemplateSpec(BaseModel):
    """Complete BMAD template specification."""
    
    template: TemplateMetadata
    workflow: WorkflowConfig = Field(default_factory=WorkflowConfig)
    sections: List[TemplateSection] = Field(default_factory=list)
    
    # Raw YAML for reference
    raw_yaml: Optional[Dict[str, Any]] = None


class TemplateSession(BaseModel):
    """State for template-driven document generation."""
    
    template_id: str
    current_section_path: List[str] = Field(default_factory=list)
    completed_sections: List[str] = Field(default_factory=list)
    variables: Dict[str, str] = Field(default_factory=dict)
    choices: Dict[str, str] = Field(default_factory=dict)
    generated_content: Dict[str, str] = Field(default_factory=dict)

"""Pydantic models for BMAD agent specifications."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentMetadata(BaseModel):
    """Agent metadata from YAML block."""
    
    name: Optional[str] = None
    id: str
    title: str
    icon: Optional[str] = None
    whenToUse: Optional[str] = Field(None, alias="when_to_use")


class PersonaSpec(BaseModel):
    """Agent persona definition."""
    
    role: str
    identity: Optional[str] = None
    core_principles: Optional[List[str]] = None
    behavioral_traits: Optional[List[str]] = None
    communication_style: Optional[List[str]] = None
    expertise: Optional[List[str]] = None


class CommandSpec(BaseModel):
    """Command specification."""
    
    name: str
    description: str
    
    @classmethod
    def from_string(cls, cmd_str: str) -> "CommandSpec":
        """Parse command from 'name: description' format."""
        parts = cmd_str.split(":", 1)
        if len(parts) == 2:
            return cls(name=parts[0].strip(), description=parts[1].strip())
        return cls(name=parts[0].strip(), description="")


class DependenciesSpec(BaseModel):
    """Agent dependencies (tasks, templates, checklists, data)."""
    
    tasks: List[str] = Field(default_factory=list)
    templates: List[str] = Field(default_factory=list)
    checklists: List[str] = Field(default_factory=list)
    data: List[str] = Field(default_factory=list)
    utils: List[str] = Field(default_factory=list)


class AgentSpec(BaseModel):
    """Complete BMAD agent specification."""
    
    # Metadata
    agent: AgentMetadata
    persona: PersonaSpec
    
    # Instructions
    activation_instructions: List[str] = Field(default_factory=list)
    ide_file_resolution: Optional[List[str]] = None
    request_resolution: Optional[str] = None
    
    # Capabilities
    commands: List[CommandSpec] = Field(default_factory=list)
    dependencies: DependenciesSpec = Field(default_factory=DependenciesSpec)
    
    # Raw content for reference
    raw_yaml: Optional[Dict[str, Any]] = None
    raw_markdown: Optional[str] = None


class BMADConfig(BaseModel):
    """BMAD core configuration from core-config.yaml."""
    
    prdVersion: Optional[str] = None
    prdSharded: Optional[bool] = None
    prdShardedLocation: Optional[str] = None
    epicFilePattern: Optional[str] = None
    architectureVersion: Optional[str] = None
    architectureSharded: Optional[bool] = None
    architectureShardedLocation: Optional[str] = None
    devLoadAlwaysFiles: List[str] = Field(default_factory=list)
    devDebugLog: Optional[str] = None
    agentCoreDump: Optional[str] = None

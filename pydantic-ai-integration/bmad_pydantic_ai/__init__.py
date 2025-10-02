"""BMAD Pydantic AI Integration Package.

This package provides an integration layer between BMAD's markdown/YAML 
agent definitions and the Pydantic AI framework.
"""

from .composers import SystemPromptComposer
from .models import (
    AgentSpec,
    ElicitationSession,
    TemplateSession,
    TemplateSpec,
    TaskSpec,
)
from .parsers import BMADAgentParser, BMADTaskParser, BMADTemplateParser
from .registry import AgentRegistry, ToolRegistry
from .state import SessionManager, WorkflowState
from .tools import ElicitationEngine, TaskRunner, TemplateDriver

__version__ = "0.1.0"

__all__ = [
    # Parsers
    "BMADAgentParser",
    "BMADTaskParser",
    "BMADTemplateParser",
    # Models
    "AgentSpec",
    "TaskSpec",
    "TemplateSpec",
    "ElicitationSession",
    "TemplateSession",
    # Composers
    "SystemPromptComposer",
    # Tools
    "TaskRunner",
    "TemplateDriver",
    "ElicitationEngine",
    # State
    "SessionManager",
    "WorkflowState",
    # Registry
    "AgentRegistry",
    "ToolRegistry",
]

"""Session state management for BMAD workflows."""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from ..models import ElicitationSession, TemplateSession


class WorkflowState(BaseModel):
    """State for a complete workflow session."""

    session_id: str
    agent_id: str
    current_command: Optional[str] = None

    # Template session if active
    template_session: Optional[TemplateSession] = None

    # Elicitation session if active
    elicitation_session: Optional[ElicitationSession] = None

    # User selections and choices
    user_choices: Dict[str, Any] = Field(default_factory=dict)

    # Context variables
    variables: Dict[str, str] = Field(default_factory=dict)

    # Workflow history
    command_history: list[str] = Field(default_factory=list)


class SessionManager:
    """Manage workflow sessions and state."""

    def __init__(self):
        """Initialize session manager."""
        self._sessions: Dict[str, WorkflowState] = {}

    def create_session(self, session_id: str, agent_id: str) -> WorkflowState:
        """Create a new workflow session.
        
        Args:
            session_id: Unique session identifier
            agent_id: ID of the agent for this session
            
        Returns:
            New WorkflowState object
        """
        state = WorkflowState(session_id=session_id, agent_id=agent_id)
        self._sessions[session_id] = state
        return state

    def get_session(self, session_id: str) -> Optional[WorkflowState]:
        """Get an existing session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            WorkflowState or None if not found
        """
        return self._sessions.get(session_id)

    def update_session(self, session_id: str, state: WorkflowState) -> None:
        """Update an existing session.
        
        Args:
            session_id: Session identifier
            state: Updated WorkflowState
        """
        self._sessions[session_id] = state

    def delete_session(self, session_id: str) -> None:
        """Delete a session.
        
        Args:
            session_id: Session identifier
        """
        if session_id in self._sessions:
            del self._sessions[session_id]

    def add_command_to_history(self, session_id: str, command: str) -> None:
        """Add a command to session history.
        
        Args:
            session_id: Session identifier
            command: Command executed
        """
        session = self.get_session(session_id)
        if session:
            session.command_history.append(command)
            session.current_command = command
            self.update_session(session_id, session)

    def set_template_session(
        self, session_id: str, template_session: TemplateSession
    ) -> None:
        """Set template session for workflow.
        
        Args:
            session_id: Session identifier
            template_session: Active template session
        """
        session = self.get_session(session_id)
        if session:
            session.template_session = template_session
            self.update_session(session_id, session)

    def set_elicitation_session(
        self, session_id: str, elicitation_session: ElicitationSession
    ) -> None:
        """Set elicitation session for workflow.
        
        Args:
            session_id: Session identifier
            elicitation_session: Active elicitation session
        """
        session = self.get_session(session_id)
        if session:
            session.elicitation_session = elicitation_session
            self.update_session(session_id, session)

    def set_variable(self, session_id: str, key: str, value: str) -> None:
        """Set a context variable.
        
        Args:
            session_id: Session identifier
            key: Variable name
            value: Variable value
        """
        session = self.get_session(session_id)
        if session:
            session.variables[key] = value
            self.update_session(session_id, session)

    def get_variable(self, session_id: str, key: str) -> Optional[str]:
        """Get a context variable.
        
        Args:
            session_id: Session identifier
            key: Variable name
            
        Returns:
            Variable value or None
        """
        session = self.get_session(session_id)
        if session:
            return session.variables.get(key)
        return None

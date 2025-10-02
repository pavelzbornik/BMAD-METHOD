"""System prompt composer for BMAD agents."""

from typing import List, Optional

from ..models import AgentSpec


class SystemPromptComposer:
    """Compose system prompts from BMAD agent specifications."""

    def compose(self, agent_spec: AgentSpec, include_commands: bool = True) -> str:
        """Compose a system prompt from agent specification.
        
        Args:
            agent_spec: Parsed agent specification
            include_commands: Whether to include available commands in prompt
            
        Returns:
            Composed system prompt string
        """
        parts = []
        
        # Agent identity
        parts.append(self._compose_identity(agent_spec))
        
        # Persona and principles
        parts.append(self._compose_persona(agent_spec))
        
        # Activation instructions
        if agent_spec.activation_instructions:
            parts.append(self._compose_activation(agent_spec))
        
        # Commands (if requested)
        if include_commands and agent_spec.commands:
            parts.append(self._compose_commands(agent_spec))
        
        # Context minimization reminder
        parts.append(self._compose_context_rules(agent_spec))
        
        return "\n\n".join(parts)
    
    def _compose_identity(self, agent_spec: AgentSpec) -> str:
        """Compose agent identity section."""
        agent = agent_spec.agent
        parts = [f"# {agent.title}"]
        
        if agent.icon:
            parts[0] = f"{agent.icon} {parts[0]}"
        
        if agent.name:
            parts.append(f"Name: {agent.name}")
        
        if agent.whenToUse:
            parts.append(f"\n**When to use this agent:** {agent.whenToUse}")
        
        return "\n".join(parts)
    
    def _compose_persona(self, agent_spec: AgentSpec) -> str:
        """Compose persona section."""
        persona = agent_spec.persona
        parts = ["## Persona"]
        
        parts.append(f"**Role:** {persona.role}")
        
        if persona.identity:
            parts.append(f"**Identity:** {persona.identity}")
        
        if persona.core_principles:
            parts.append("\n**Core Principles:**")
            for principle in persona.core_principles:
                parts.append(f"- {principle}")
        
        if persona.behavioral_traits:
            parts.append("\n**Behavioral Traits:**")
            for trait in persona.behavioral_traits:
                parts.append(f"- {trait}")
        
        if persona.communication_style:
            parts.append("\n**Communication Style:**")
            for style in persona.communication_style:
                parts.append(f"- {style}")
        
        if persona.expertise:
            parts.append("\n**Expertise:**")
            for exp in persona.expertise:
                parts.append(f"- {exp}")
        
        return "\n".join(parts)
    
    def _compose_activation(self, agent_spec: AgentSpec) -> str:
        """Compose activation instructions section."""
        parts = ["## Activation Instructions"]
        
        for idx, instruction in enumerate(agent_spec.activation_instructions, 1):
            parts.append(f"{idx}. {instruction}")
        
        return "\n".join(parts)
    
    def _compose_commands(self, agent_spec: AgentSpec) -> str:
        """Compose available commands section."""
        parts = ["## Available Commands"]
        parts.append("All commands require * prefix (e.g., *help)")
        parts.append("")
        
        for idx, cmd in enumerate(agent_spec.commands, 1):
            parts.append(f"{idx}. **{cmd.name}**: {cmd.description}")
        
        return "\n".join(parts)
    
    def _compose_context_rules(self, agent_spec: AgentSpec) -> str:
        """Compose context minimization rules."""
        parts = ["## Critical Context Rules"]
        parts.append("- ONLY load dependency files when user explicitly requests command execution")
        parts.append("- Never pre-load tasks, templates, or data files during startup")
        parts.append("- Respect lazy-loading principles for context minimization")
        parts.append("- Tasks with elicit=true REQUIRE user interaction - never skip")
        
        return "\n".join(parts)

"""Parser for BMAD agent markdown files."""

import re
from pathlib import Path
from typing import Optional

import yaml

from ..models import AgentMetadata, AgentSpec, CommandSpec, DependenciesSpec, PersonaSpec


class BMADAgentParser:
    """Parse BMAD agent markdown files into structured AgentSpec objects."""

    def parse_agent_file(self, file_path: str) -> AgentSpec:
        """Parse a BMAD agent markdown file.
        
        Args:
            file_path: Path to the agent markdown file
            
        Returns:
            Structured AgentSpec object
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Agent file not found: {file_path}")
        
        content = path.read_text()
        return self.parse_agent_content(content)
    
    def parse_agent_content(self, content: str) -> AgentSpec:
        """Parse BMAD agent content from markdown string.
        
        Args:
            content: Raw markdown content
            
        Returns:
            Structured AgentSpec object
        """
        # Extract YAML block
        yaml_block = self._extract_yaml_block(content)
        if not yaml_block:
            raise ValueError("No YAML block found in agent file")
        
        # Parse YAML
        try:
            yaml_data = yaml.safe_load(yaml_block)
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse YAML: {e}")
        
        # Build AgentSpec
        return self._build_agent_spec(yaml_data, content)
    
    def _extract_yaml_block(self, content: str) -> Optional[str]:
        """Extract YAML block from markdown content."""
        # Look for ```yaml ... ``` block
        pattern = r"```yaml\s*\n(.*?)\n```"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.group(1)
        return None
    
    def _build_agent_spec(self, yaml_data: dict, raw_content: str) -> AgentSpec:
        """Build AgentSpec from parsed YAML data."""
        # Parse agent metadata
        agent_meta = AgentMetadata(**yaml_data.get("agent", {}))
        
        # Parse persona
        persona_data = yaml_data.get("persona", {})
        persona = PersonaSpec(**persona_data)
        
        # Parse commands
        commands = []
        for cmd in yaml_data.get("commands", []):
            if isinstance(cmd, str):
                commands.append(CommandSpec.from_string(cmd))
            elif isinstance(cmd, dict):
                # Commands are in format {name: description}
                for name, description in cmd.items():
                    commands.append(CommandSpec(name=name, description=description))
        
        # Parse dependencies
        deps_data = yaml_data.get("dependencies", {})
        dependencies = DependenciesSpec(**deps_data)
        
        # Parse activation instructions - handle mixed string and dict format
        activation_instructions = []
        for item in yaml_data.get("activation-instructions", []):
            if isinstance(item, str):
                activation_instructions.append(item)
            elif isinstance(item, dict):
                # Convert dict to string format
                for key, value in item.items():
                    activation_instructions.append(f"{key}: {value}")
        
        # Parse other fields - handle mixed format
        ide_file_resolution = []
        for item in yaml_data.get("IDE-FILE-RESOLUTION", []):
            if isinstance(item, str):
                ide_file_resolution.append(item)
            elif isinstance(item, dict):
                for key, value in item.items():
                    ide_file_resolution.append(f"{key}: {value}")
        
        request_resolution = yaml_data.get("REQUEST-RESOLUTION")
        
        return AgentSpec(
            agent=agent_meta,
            persona=persona,
            commands=commands,
            dependencies=dependencies,
            activation_instructions=activation_instructions,
            ide_file_resolution=ide_file_resolution if ide_file_resolution else None,
            request_resolution=request_resolution,
            raw_yaml=yaml_data,
            raw_markdown=raw_content,
        )

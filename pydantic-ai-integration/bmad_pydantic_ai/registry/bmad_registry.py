"""Registry for BMAD agents and tools."""

from pathlib import Path
from typing import Dict, List, Optional

from ..models import AgentSpec
from ..parsers import BMADAgentParser


class AgentRegistry:
    """Registry for discovering and managing BMAD agents."""

    def __init__(self, root_path: str):
        """Initialize agent registry.
        
        Args:
            root_path: Root path to BMAD installation
        """
        self.root_path = Path(root_path)
        self.parser = BMADAgentParser()
        self._agents: Dict[str, AgentSpec] = {}

    def discover_agents(self, include_expansion_packs: bool = True) -> None:
        """Discover and register all available agents.
        
        Args:
            include_expansion_packs: Whether to scan expansion packs
        """
        # Scan bmad-core agents
        core_agents_dir = self.root_path / "bmad-core" / "agents"
        if core_agents_dir.exists():
            self._scan_agent_directory(core_agents_dir)

        # Scan expansion pack agents if requested
        if include_expansion_packs:
            expansion_packs_dir = self.root_path / "expansion-packs"
            if expansion_packs_dir.exists():
                for pack_dir in expansion_packs_dir.iterdir():
                    if pack_dir.is_dir():
                        agents_dir = pack_dir / "agents"
                        if agents_dir.exists():
                            self._scan_agent_directory(agents_dir)

    def _scan_agent_directory(self, directory: Path) -> None:
        """Scan a directory for agent files.
        
        Args:
            directory: Directory to scan
        """
        for agent_file in directory.glob("*.md"):
            try:
                agent_spec = self.parser.parse_agent_file(str(agent_file))
                self._agents[agent_spec.agent.id] = agent_spec
            except Exception as e:
                # Log error but continue
                print(f"Warning: Failed to parse agent {agent_file.name}: {e}")

    def get_agent(self, agent_id: str) -> Optional[AgentSpec]:
        """Get an agent by ID.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            AgentSpec or None if not found
        """
        return self._agents.get(agent_id)

    def list_agents(self) -> List[str]:
        """List all registered agent IDs.
        
        Returns:
            List of agent IDs
        """
        return sorted(self._agents.keys())

    def list_agents_by_role(self) -> Dict[str, List[str]]:
        """List agents grouped by role.
        
        Returns:
            Dictionary mapping roles to agent IDs
        """
        by_role = {}
        for agent_id, agent_spec in self._agents.items():
            role = agent_spec.persona.role
            if role not in by_role:
                by_role[role] = []
            by_role[role].append(agent_id)
        return by_role

    def register_agent(self, agent_id: str, agent_spec: AgentSpec) -> None:
        """Manually register an agent.
        
        Args:
            agent_id: Agent identifier
            agent_spec: Agent specification
        """
        self._agents[agent_id] = agent_spec


class ToolRegistry:
    """Registry for BMAD tools (tasks, templates, checklists)."""

    def __init__(self, root_path: str):
        """Initialize tool registry.
        
        Args:
            root_path: Root path to BMAD installation
        """
        self.root_path = Path(root_path)
        self._tasks: Dict[str, str] = {}
        self._templates: Dict[str, str] = {}
        self._checklists: Dict[str, str] = {}

    def discover_tools(self, include_expansion_packs: bool = True) -> None:
        """Discover all available tools.
        
        Args:
            include_expansion_packs: Whether to scan expansion packs
        """
        # Scan bmad-core
        self._scan_tools(self.root_path / "bmad-core")

        # Scan expansion packs if requested
        if include_expansion_packs:
            expansion_packs_dir = self.root_path / "expansion-packs"
            if expansion_packs_dir.exists():
                for pack_dir in expansion_packs_dir.iterdir():
                    if pack_dir.is_dir():
                        self._scan_tools(pack_dir)

    def _scan_tools(self, base_dir: Path) -> None:
        """Scan a base directory for tools.
        
        Args:
            base_dir: Base directory to scan
        """
        # Scan tasks
        tasks_dir = base_dir / "tasks"
        if tasks_dir.exists():
            for task_file in tasks_dir.glob("*.md"):
                self._tasks[task_file.name] = str(task_file)

        # Scan templates
        templates_dir = base_dir / "templates"
        if templates_dir.exists():
            for template_file in templates_dir.glob("*.yaml"):
                self._templates[template_file.name] = str(template_file)

        # Scan checklists
        checklists_dir = base_dir / "checklists"
        if checklists_dir.exists():
            for checklist_file in checklists_dir.glob("*.md"):
                self._checklists[checklist_file.name] = str(checklist_file)

    def get_task_path(self, task_name: str) -> Optional[str]:
        """Get path to a task file.
        
        Args:
            task_name: Task filename
            
        Returns:
            Path to task file or None
        """
        return self._tasks.get(task_name)

    def get_template_path(self, template_name: str) -> Optional[str]:
        """Get path to a template file.
        
        Args:
            template_name: Template filename
            
        Returns:
            Path to template file or None
        """
        return self._templates.get(template_name)

    def list_tasks(self) -> List[str]:
        """List all available tasks.
        
        Returns:
            List of task filenames
        """
        return sorted(self._tasks.keys())

    def list_templates(self) -> List[str]:
        """List all available templates.
        
        Returns:
            List of template filenames
        """
        return sorted(self._templates.keys())

    def list_checklists(self) -> List[str]:
        """List all available checklists.
        
        Returns:
            List of checklist filenames
        """
        return sorted(self._checklists.keys())

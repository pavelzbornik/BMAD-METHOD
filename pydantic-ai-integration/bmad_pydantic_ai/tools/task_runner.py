"""Task runner tool for executing BMAD tasks."""

from pathlib import Path
from typing import Optional

from ..models import TaskSpec
from ..parsers import BMADTaskParser


class TaskRunner:
    """Execute BMAD tasks with lazy loading and elicitation support."""

    def __init__(self, root_path: str):
        """Initialize task runner.
        
        Args:
            root_path: Root path to BMAD installation (e.g., bmad-core)
        """
        self.root_path = Path(root_path)
        self.parser = BMADTaskParser()
        self._task_cache = {}
    
    def load_task(self, task_name: str) -> TaskSpec:
        """Lazy-load a task file.
        
        Args:
            task_name: Name of the task file (e.g., 'create-doc.md')
            
        Returns:
            Parsed TaskSpec object
        """
        if task_name in self._task_cache:
            return self._task_cache[task_name]
        
        task_path = self.root_path / "tasks" / task_name
        if not task_path.exists():
            raise FileNotFoundError(f"Task not found: {task_name}")
        
        task_spec = self.parser.parse_task_file(str(task_path))
        self._task_cache[task_name] = task_spec
        return task_spec
    
    def list_available_tasks(self) -> list[str]:
        """List all available tasks in the tasks directory.
        
        Returns:
            List of task filenames
        """
        tasks_dir = self.root_path / "tasks"
        if not tasks_dir.exists():
            return []
        
        return sorted([f.name for f in tasks_dir.glob("*.md")])
    
    def get_task_instructions(self, task_name: str) -> str:
        """Get formatted task instructions for display.
        
        Args:
            task_name: Name of the task file
            
        Returns:
            Formatted instructions string
        """
        task = self.load_task(task_name)
        
        parts = [f"# {task.title}"]
        
        if task.purpose:
            parts.append(f"\n## Purpose\n{task.purpose}")
        
        if task.instructions:
            parts.append("\n## Instructions")
            for idx, instruction in enumerate(task.instructions, 1):
                parts.append(f"{idx}. {instruction}")
        
        if task.elicit:
            parts.append("\n**⚠️ This task requires user interaction (elicit=true)**")
        
        return "\n".join(parts)
    
    def execute_task(self, task_name: str, context: Optional[dict] = None) -> dict:
        """Execute a task with optional context.
        
        Args:
            task_name: Name of the task file
            context: Optional context dictionary
            
        Returns:
            Execution result dictionary
        """
        task = self.load_task(task_name)
        
        return {
            "task_id": task.id,
            "title": task.title,
            "elicit": task.elicit,
            "instructions": task.instructions,
            "requires_interaction": task.elicit,
        }

"""Parser for BMAD task markdown files."""

import re
from pathlib import Path
from typing import Optional

from ..models import TaskSpec


class BMADTaskParser:
    """Parse BMAD task markdown files into structured TaskSpec objects."""

    def parse_task_file(self, file_path: str) -> TaskSpec:
        """Parse a BMAD task markdown file.
        
        Args:
            file_path: Path to the task markdown file
            
        Returns:
            Structured TaskSpec object
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Task file not found: {file_path}")
        
        content = path.read_text()
        return self.parse_task_content(content, path.stem)
    
    def parse_task_content(self, content: str, task_id: str) -> TaskSpec:
        """Parse BMAD task content from markdown string.
        
        Args:
            content: Raw markdown content
            task_id: Task identifier
            
        Returns:
            Structured TaskSpec object
        """
        # Extract title
        title = self._extract_title(content)
        
        # Extract purpose
        purpose = self._extract_purpose(content)
        
        # Extract instructions
        instructions = self._extract_instructions(content)
        
        # Check for elicit flag
        elicit = "elicit: true" in content or "elicit=true" in content
        
        return TaskSpec(
            id=task_id,
            title=title or task_id,
            purpose=purpose,
            elicit=elicit,
            instructions=instructions,
            raw_markdown=content,
        )
    
    def _extract_title(self, content: str) -> Optional[str]:
        """Extract title from markdown content."""
        # Look for first H1 heading
        pattern = r"^#\s+(.+)$"
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return None
    
    def _extract_purpose(self, content: str) -> Optional[str]:
        """Extract purpose section from markdown content."""
        # Look for ## Purpose section
        pattern = r"##\s+Purpose\s*\n\n(.*?)(?=\n##|\Z)"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None
    
    def _extract_instructions(self, content: str) -> list:
        """Extract task instructions from markdown content."""
        instructions = []
        
        # Look for task instructions sections
        pattern = r"##\s+Task Instructions\s*\n\n(.*?)(?=\n##|\Z)"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            inst_text = match.group(1).strip()
            # Split by numbered sections or bullet points
            for line in inst_text.split("\n"):
                line = line.strip()
                if line and not line.startswith("#"):
                    instructions.append(line)
        
        return instructions

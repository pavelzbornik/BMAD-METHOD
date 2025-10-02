"""Template driver for section-by-section document generation."""

from pathlib import Path
from typing import Optional

from ..models import TemplateSection, TemplateSession, TemplateSpec
from ..parsers import BMADTemplateParser


class TemplateDriver:
    """Drive template-based document generation section by section."""

    def __init__(self, root_path: str):
        """Initialize template driver.
        
        Args:
            root_path: Root path to BMAD installation (e.g., bmad-core)
        """
        self.root_path = Path(root_path)
        self.parser = BMADTemplateParser()
        self._template_cache = {}
    
    def load_template(self, template_name: str) -> TemplateSpec:
        """Lazy-load a template file.
        
        Args:
            template_name: Name of the template file (e.g., 'prd-tmpl.yaml')
            
        Returns:
            Parsed TemplateSpec object
        """
        if template_name in self._template_cache:
            return self._template_cache[template_name]
        
        template_path = self.root_path / "templates" / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")
        
        template_spec = self.parser.parse_template_file(str(template_path))
        self._template_cache[template_name] = template_spec
        return template_spec
    
    def list_available_templates(self) -> list[str]:
        """List all available templates.
        
        Returns:
            List of template filenames
        """
        templates_dir = self.root_path / "templates"
        if not templates_dir.exists():
            return []
        
        return sorted([f.name for f in templates_dir.glob("*.yaml")])
    
    def create_session(self, template_name: str) -> TemplateSession:
        """Create a new template session.
        
        Args:
            template_name: Name of the template to use
            
        Returns:
            New TemplateSession object
        """
        template = self.load_template(template_name)
        return TemplateSession(template_id=template.template.id)
    
    def get_next_section(
        self, template_name: str, session: TemplateSession
    ) -> Optional[TemplateSection]:
        """Get the next section to process.
        
        Args:
            template_name: Name of the template
            session: Current template session
            
        Returns:
            Next TemplateSection or None if complete
        """
        template = self.load_template(template_name)
        
        # Find next uncompleted section
        for section in self._iterate_sections(template.sections):
            if section.id not in session.completed_sections:
                # Check condition if present
                if section.condition:
                    # Would evaluate condition here
                    pass
                return section
        
        return None
    
    def _iterate_sections(self, sections: list[TemplateSection]):
        """Recursively iterate through sections."""
        for section in sections:
            yield section
            yield from self._iterate_sections(section.sections)
    
    def format_section_prompt(self, section: TemplateSection) -> str:
        """Format a section for LLM generation.
        
        Args:
            section: Section to format
            
        Returns:
            Formatted prompt string
        """
        parts = [f"## {section.title}"]
        
        if section.instruction:
            parts.append(f"\n**Instructions:**\n{section.instruction}")
        
        if section.type:
            parts.append(f"\n**Type:** {section.type}")
        
        if section.examples:
            parts.append("\n**Examples:**")
            for example in section.examples:
                parts.append(f"- {example}")
        
        if section.template:
            parts.append(f"\n**Template:** {section.template}")
        
        if section.choices:
            parts.append("\n**Choices:**")
            for choice_name, options in section.choices.items():
                parts.append(f"- {choice_name}: {', '.join(options)}")
        
        if section.elicit:
            parts.append("\n**🔄 Elicitation will be offered after this section**")
        
        return "\n".join(parts)

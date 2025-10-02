"""Parser for BMAD template YAML files."""

from pathlib import Path
from typing import Any, Dict

import yaml

from ..models import TemplateMetadata, TemplateSection, TemplateSpec, WorkflowConfig


class BMADTemplateParser:
    """Parse BMAD template YAML files into structured TemplateSpec objects."""

    def parse_template_file(self, file_path: str) -> TemplateSpec:
        """Parse a BMAD template YAML file.
        
        Args:
            file_path: Path to the template YAML file
            
        Returns:
            Structured TemplateSpec object
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Template file not found: {file_path}")
        
        content = path.read_text()
        return self.parse_template_content(content)
    
    def parse_template_content(self, content: str) -> TemplateSpec:
        """Parse BMAD template content from YAML string.
        
        Args:
            content: Raw YAML content
            
        Returns:
            Structured TemplateSpec object
        """
        try:
            yaml_data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse YAML: {e}")
        
        return self._build_template_spec(yaml_data)
    
    def _build_template_spec(self, yaml_data: Dict[str, Any]) -> TemplateSpec:
        """Build TemplateSpec from parsed YAML data."""
        # Parse template metadata - handle version as number
        template_data = yaml_data.get("template", {}).copy()
        if "version" in template_data and not isinstance(template_data["version"], str):
            template_data["version"] = str(template_data["version"])
        template_meta = TemplateMetadata(**template_data)
        
        # Parse workflow configuration
        workflow_data = yaml_data.get("workflow", {})
        workflow = WorkflowConfig(**workflow_data)
        
        # Parse sections recursively
        sections_data = yaml_data.get("sections", [])
        sections = [self._parse_section(section) for section in sections_data]
        
        return TemplateSpec(
            template=template_meta,
            workflow=workflow,
            sections=sections,
            raw_yaml=yaml_data,
        )
    
    def _parse_section(self, section_data: Dict[str, Any]) -> TemplateSection:
        """Parse a single section recursively."""
        # Extract nested sections
        nested_sections_data = section_data.pop("sections", [])
        
        # Create section
        section = TemplateSection(**section_data)
        
        # Parse nested sections recursively
        section.sections = [self._parse_section(s) for s in nested_sections_data]
        
        return section

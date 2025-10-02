"""Example: Parse a BMAD template and display section structure."""

from pathlib import Path

from bmad_pydantic_ai import BMADTemplateParser, TemplateDriver


def display_section(section, indent=0):
    """Recursively display section structure."""
    prefix = "  " * indent
    print(f"{prefix}📄 {section.title} (id: {section.id})")
    
    if section.type:
        print(f"{prefix}   Type: {section.type}")
    
    if section.elicit:
        print(f"{prefix}   🔄 Elicitation enabled")
    
    if section.condition:
        print(f"{prefix}   ⚠️  Conditional: {section.condition}")
    
    if section.examples:
        print(f"{prefix}   📝 {len(section.examples)} example(s)")
    
    # Display nested sections
    for subsection in section.sections:
        display_section(subsection, indent + 1)


def main():
    """Parse PRD template and display structure."""
    # Initialize parser
    parser = BMADTemplateParser()
    
    # Get path to PRD template
    repo_root = Path(__file__).parent.parent.parent
    template_file = repo_root / "bmad-core" / "templates" / "prd-tmpl.yaml"
    
    print(f"Parsing template file: {template_file}")
    print("=" * 80)
    
    # Parse the template
    template_spec = parser.parse_template_file(str(template_file))
    
    # Display template information
    print(f"\n✓ Successfully parsed template: {template_spec.template.id}")
    print(f"  Name: {template_spec.template.name}")
    print(f"  Version: {template_spec.template.version}")
    print(f"  Output format: {template_spec.template.output.get('format', 'N/A')}")
    
    # Display workflow configuration
    print(f"\n⚙️  Workflow:")
    print(f"  Mode: {template_spec.workflow.mode}")
    print(f"  Elicitation: {template_spec.workflow.elicitation or 'None'}")
    
    # Display section structure
    print(f"\n📋 Section Structure ({len(template_spec.sections)} top-level sections):")
    for section in template_spec.sections:
        display_section(section)
    
    # Test template driver
    print("\n" + "=" * 80)
    print("TEMPLATE DRIVER TEST")
    print("=" * 80)
    
    driver = TemplateDriver(str(repo_root / "bmad-core"))
    session = driver.create_session("prd-tmpl.yaml")
    
    print(f"\n✓ Created template session: {session.template_id}")
    
    # Get first section
    next_section = driver.get_next_section("prd-tmpl.yaml", session)
    if next_section:
        print(f"\n📍 Next section to process: {next_section.title}")
        print("\nFormatted prompt:")
        print("-" * 80)
        prompt = driver.format_section_prompt(next_section)
        preview = prompt[:500]
        print(preview)
        if len(prompt) > 500:
            print(f"\n... ({len(prompt) - 500} more characters)")


if __name__ == "__main__":
    main()

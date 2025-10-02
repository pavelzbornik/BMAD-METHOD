"""Example: Parse and display a BMAD agent specification."""

from pathlib import Path

from bmad_pydantic_ai import BMADAgentParser, SystemPromptComposer


def main():
    """Parse PM agent and display structured information."""
    # Initialize parser
    parser = BMADAgentParser()
    
    # Get path to PM agent
    repo_root = Path(__file__).parent.parent.parent
    agent_file = repo_root / "bmad-core" / "agents" / "pm.md"
    
    print(f"Parsing agent file: {agent_file}")
    print("=" * 80)
    
    # Parse the agent
    agent_spec = parser.parse_agent_file(str(agent_file))
    
    # Display agent information
    print(f"\n✓ Successfully parsed agent: {agent_spec.agent.id}")
    print(f"  Title: {agent_spec.agent.title}")
    print(f"  Icon: {agent_spec.agent.icon}")
    print(f"  Role: {agent_spec.persona.role}")
    
    # Display commands
    print(f"\n📋 Commands ({len(agent_spec.commands)}):")
    for idx, cmd in enumerate(agent_spec.commands[:5], 1):
        print(f"  {idx}. *{cmd.name}: {cmd.description}")
    if len(agent_spec.commands) > 5:
        print(f"  ... and {len(agent_spec.commands) - 5} more")
    
    # Display dependencies
    print(f"\n📦 Dependencies:")
    print(f"  Tasks: {len(agent_spec.dependencies.tasks)}")
    print(f"  Templates: {len(agent_spec.dependencies.templates)}")
    print(f"  Checklists: {len(agent_spec.dependencies.checklists)}")
    print(f"  Data: {len(agent_spec.dependencies.data)}")
    
    # Generate system prompt
    print("\n" + "=" * 80)
    print("SYSTEM PROMPT PREVIEW")
    print("=" * 80)
    
    composer = SystemPromptComposer()
    system_prompt = composer.compose(agent_spec, include_commands=True)
    
    # Display first 1000 chars of system prompt
    preview = system_prompt[:1000]
    print(preview)
    if len(system_prompt) > 1000:
        print(f"\n... ({len(system_prompt) - 1000} more characters)")
    
    print("\n" + "=" * 80)
    print(f"✓ Complete system prompt is {len(system_prompt)} characters")


if __name__ == "__main__":
    main()

"""Example: Discover and list all BMAD agents and tools."""

from pathlib import Path

from bmad_pydantic_ai import AgentRegistry, ToolRegistry


def main():
    """Discover all agents and tools in the BMAD repository."""
    repo_root = Path(__file__).parent.parent.parent
    
    print("BMAD Discovery Demo")
    print("=" * 80)
    
    # Initialize registries
    agent_registry = AgentRegistry(str(repo_root))
    tool_registry = ToolRegistry(str(repo_root))
    
    # Discover agents
    print("\n🔍 Discovering agents...")
    agent_registry.discover_agents(include_expansion_packs=True)
    
    agents = agent_registry.list_agents()
    print(f"✓ Found {len(agents)} agents")
    
    # List agents by role
    print("\n" + "=" * 80)
    print("AGENTS BY ROLE")
    print("=" * 80)
    
    by_role = agent_registry.list_agents_by_role()
    for role, agent_ids in sorted(by_role.items()):
        print(f"\n{role}:")
        for agent_id in agent_ids:
            agent = agent_registry.get_agent(agent_id)
            if agent:
                icon = agent.agent.icon or "📋"
                print(f"  {icon} {agent.agent.title} ({agent_id})")
    
    # Discover tools
    print("\n" + "=" * 80)
    print("DISCOVERING TOOLS")
    print("=" * 80)
    
    print("\n🔍 Discovering tasks, templates, and checklists...")
    tool_registry.discover_tools(include_expansion_packs=True)
    
    # List tasks
    tasks = tool_registry.list_tasks()
    print(f"\n📋 Tasks ({len(tasks)}):")
    for idx, task in enumerate(tasks[:10], 1):
        print(f"  {idx}. {task}")
    if len(tasks) > 10:
        print(f"  ... and {len(tasks) - 10} more")
    
    # List templates
    templates = tool_registry.list_templates()
    print(f"\n📄 Templates ({len(templates)}):")
    for idx, template in enumerate(templates[:10], 1):
        print(f"  {idx}. {template}")
    if len(templates) > 10:
        print(f"  ... and {len(templates) - 10} more")
    
    # List checklists
    checklists = tool_registry.list_checklists()
    print(f"\n✅ Checklists ({len(checklists)}):")
    for idx, checklist in enumerate(checklists[:10], 1):
        print(f"  {idx}. {checklist}")
    if len(checklists) > 10:
        print(f"  ... and {len(checklists) - 10} more")
    
    # Show example agent details
    print("\n" + "=" * 80)
    print("EXAMPLE AGENT DETAILS: PM")
    print("=" * 80)
    
    pm_agent = agent_registry.get_agent("pm")
    if pm_agent:
        print(f"\n{pm_agent.agent.icon} {pm_agent.agent.title}")
        print(f"ID: {pm_agent.agent.id}")
        print(f"Role: {pm_agent.persona.role}")
        print(f"\nCommands: {len(pm_agent.commands)}")
        for cmd in pm_agent.commands[:5]:
            print(f"  - *{cmd.name}")
        
        print(f"\nAvailable Tasks: {len(pm_agent.dependencies.tasks)}")
        for task in pm_agent.dependencies.tasks[:5]:
            print(f"  - {task}")
        
        print(f"\nAvailable Templates: {len(pm_agent.dependencies.templates)}")
        for template in pm_agent.dependencies.templates[:5]:
            print(f"  - {template}")


if __name__ == "__main__":
    main()

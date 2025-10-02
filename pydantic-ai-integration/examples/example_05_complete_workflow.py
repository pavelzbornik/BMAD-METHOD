"""
Example: Complete workflow with Pydantic AI agent using BMAD integration.

This example demonstrates:
1. Loading a BMAD agent specification
2. Creating a pydantic-ai Agent with BMAD system prompt
3. Using BMAD tools (task runner, template driver) as agent tools
4. Executing a complete workflow: command -> task -> template -> elicitation
"""

import asyncio
from pathlib import Path
from typing import Optional

from pydantic_ai import Agent, RunContext
from pydantic_ai.models import KnownModelName

from bmad_pydantic_ai import (
    AgentRegistry,
    BMADAgentParser,
    ElicitationEngine,
    SessionManager,
    SystemPromptComposer,
    TaskRunner,
    TemplateDriver,
)


# Define dependencies for the agent
class BMADDependencies:
    """Dependencies providing access to BMAD tools."""

    def __init__(self, root_path: str):
        self.root_path = root_path
        self.task_runner = TaskRunner(root_path)
        self.template_driver = TemplateDriver(root_path)
        self.elicitation_engine = ElicitationEngine()
        self.session_manager = SessionManager()
        self.agent_registry = AgentRegistry(Path(root_path).parent)


async def create_bmad_agent(
    agent_id: str,
    root_path: str,
    model: KnownModelName = "openai:gpt-4",
) -> tuple[Agent, BMADDependencies]:
    """Create a pydantic-ai agent from BMAD specification.
    
    Args:
        agent_id: BMAD agent ID (e.g., 'pm')
        root_path: Path to bmad-core directory
        model: LLM model to use
        
    Returns:
        Tuple of (pydantic-ai Agent, BMAD dependencies)
    """
    # Parse BMAD agent
    parser = BMADAgentParser()
    agent_file = Path(root_path) / "agents" / f"{agent_id}.md"
    agent_spec = parser.parse_agent_file(str(agent_file))

    # Compose system prompt
    composer = SystemPromptComposer()
    system_prompt = composer.compose(agent_spec, include_commands=True)

    # Create dependencies
    deps = BMADDependencies(root_path)

    # Create pydantic-ai agent
    agent = Agent(
        model,
        deps_type=BMADDependencies,
        system_prompt=system_prompt,
    )

    # Register BMAD tools
    register_bmad_tools(agent)

    return agent, deps


def register_bmad_tools(agent: Agent):
    """Register BMAD tools with the pydantic-ai agent."""

    @agent.tool
    async def list_tasks(ctx: RunContext[BMADDependencies]) -> str:
        """List all available BMAD tasks."""
        tasks = ctx.deps.task_runner.list_available_tasks()
        return "Available tasks:\n" + "\n".join(f"  {i+1}. {t}" for i, t in enumerate(tasks))

    @agent.tool
    async def execute_task(ctx: RunContext[BMADDependencies], task_name: str) -> str:
        """Execute a BMAD task by name.
        
        Args:
            task_name: Name of the task file (e.g., 'create-doc.md')
        """
        instructions = ctx.deps.task_runner.get_task_instructions(task_name)
        return f"Task: {task_name}\n\n{instructions}"

    @agent.tool
    async def list_templates(ctx: RunContext[BMADDependencies]) -> str:
        """List all available BMAD templates."""
        templates = ctx.deps.template_driver.list_available_templates()
        return "Available templates:\n" + "\n".join(
            f"  {i+1}. {t}" for i, t in enumerate(templates)
        )

    @agent.tool
    async def start_template(
        ctx: RunContext[BMADDependencies], template_name: str, session_id: str
    ) -> str:
        """Start a template-driven document generation session.
        
        Args:
            template_name: Name of the template file (e.g., 'prd-tmpl.yaml')
            session_id: Unique session identifier
        """
        # Load template
        template = ctx.deps.template_driver.load_template(template_name)

        # Create session
        session = ctx.deps.template_driver.create_session(template_name)
        ctx.deps.session_manager.set_template_session(session_id, session)

        # Get first section
        next_section = ctx.deps.template_driver.get_next_section(template_name, session)
        if next_section:
            prompt = ctx.deps.template_driver.format_section_prompt(next_section)
            return (
                f"Started template: {template.template.name}\n\n"
                f"Next section: {next_section.title}\n\n{prompt}"
            )

        return f"Started template: {template.template.name} (no sections to process)"

    @agent.tool
    async def offer_elicitation(
        ctx: RunContext[BMADDependencies],
        content: str,
        content_type: str = "general",
        session_id: Optional[str] = None,
    ) -> str:
        """Offer elicitation methods for content review.
        
        Args:
            content: Content to apply elicitation to
            content_type: Type of content (technical, user-facing, strategic, creative)
            session_id: Optional session ID to track state
        """
        # Create elicitation session
        session = ctx.deps.elicitation_engine.create_session(content, content_type)

        if session_id:
            ctx.deps.session_manager.set_elicitation_session(session_id, session)

        # Format menu
        menu = ctx.deps.elicitation_engine.format_menu(session)
        return menu

    @agent.tool
    async def apply_elicitation_method(
        ctx: RunContext[BMADDependencies],
        method_index: int,
        content: str,
        session_id: str,
    ) -> str:
        """Apply an elicitation method to content.
        
        Args:
            method_index: Index of the method to apply (0-8)
            content: Content to apply method to
            session_id: Session ID to retrieve elicitation session
        """
        # Get session
        workflow_state = ctx.deps.session_manager.get_session(session_id)
        if not workflow_state or not workflow_state.elicitation_session:
            return "Error: No active elicitation session found"

        session = workflow_state.elicitation_session

        # Check if proceed was selected
        if method_index >= len(session.available_methods):
            return "Proceeding without further elicitation."

        # Apply method
        method = session.available_methods[method_index]
        result = ctx.deps.elicitation_engine.apply_method(session, method.id, content)

        return (
            f"Applied: {result['method']}\n\n"
            f"Iteration: {result['iteration']}\n\n"
            f"Prompt:\n{result['prompt']}"
        )


async def demo_workflow():
    """Demonstrate a complete BMAD workflow with pydantic-ai."""
    print("=" * 80)
    print("BMAD + Pydantic AI Integration Demo")
    print("=" * 80)

    # Get paths
    repo_root = Path(__file__).parent.parent.parent
    bmad_core = repo_root / "bmad-core"

    print(f"\n📁 BMAD Core: {bmad_core}")

    # Parse agent to show what we would create
    print("\n🤖 Loading PM agent specification...")
    agent_spec = BMADAgentParser().parse_agent_file(str(bmad_core / "agents" / "pm.md"))
    print("✓ Agent specification loaded successfully")

    # Show agent info
    print(f"\n{agent_spec.agent.icon} {agent_spec.agent.title}")
    print(f"ID: {agent_spec.agent.id}")
    print(f"Role: {agent_spec.persona.role}")
    print(f"Commands: {len(agent_spec.commands)}")
    print(f"Dependencies: {len(agent_spec.dependencies.tasks)} tasks, {len(agent_spec.dependencies.templates)} templates")
    
    # Generate system prompt
    composer = SystemPromptComposer()
    system_prompt = composer.compose(agent_spec, include_commands=True)
    print(f"\n📝 Generated system prompt: {len(system_prompt)} characters")
    
    # Show what tools would be registered
    print("\n🔧 BMAD Tools that would be registered:")
    print("  - list_tasks: List all available BMAD tasks")
    print("  - execute_task: Execute a BMAD task by name")
    print("  - list_templates: List all available BMAD templates")
    print("  - start_template: Start template-driven document generation")
    print("  - offer_elicitation: Offer elicitation methods for content review")
    print("  - apply_elicitation_method: Apply an elicitation method to content")
    
    # Create dependencies (without actual agent)
    deps = BMADDependencies(str(bmad_core))

    # Demo 1: List tasks
    print("\n" + "=" * 80)
    print("DEMO 1: List Available Tasks")
    print("=" * 80)

    tasks = deps.task_runner.list_available_tasks()
    print(f"Available tasks ({len(tasks)}):")
    for i, task in enumerate(tasks[:10], 1):
        print(f"  {i}. {task}")
    if len(tasks) > 10:
        print(f"  ... and {len(tasks) - 10} more")

    # Demo 2: List templates
    print("\n" + "=" * 80)
    print("DEMO 2: List Available Templates")
    print("=" * 80)

    templates = deps.template_driver.list_available_templates()
    print(f"Available templates ({len(templates)}):")
    for i, template in enumerate(templates, 1):
        print(f"  {i}. {template}")

    # Demo 3: Show elicitation options
    print("\n" + "=" * 80)
    print("DEMO 3: Elicitation Engine")
    print("=" * 80)

    example_content = """
    FR1: The system shall support user authentication
    FR2: The system shall maintain audit logs
    FR3: The system shall provide role-based access control
    """

    elicitation_session = deps.elicitation_engine.create_session(
        example_content, "technical"
    )
    menu = deps.elicitation_engine.format_menu(elicitation_session)
    print(menu)
    
    # Demo 4: Show what template session would look like
    print("\n" + "=" * 80)
    print("DEMO 4: Template Session Example")
    print("=" * 80)
    
    print("\n📄 Loading PRD template...")
    template = deps.template_driver.load_template("prd-tmpl.yaml")
    print(f"✓ Template: {template.template.name}")
    print(f"  Workflow mode: {template.workflow.mode}")
    print(f"  Elicitation: {template.workflow.elicitation}")
    print(f"  Sections: {len(template.sections)}")
    
    session = deps.template_driver.create_session("prd-tmpl.yaml")
    next_section = deps.template_driver.get_next_section("prd-tmpl.yaml", session)
    if next_section:
        print(f"\n📍 First section to process: {next_section.title}")
        print(f"  Has nested sections: {len(next_section.sections)}")
        print(f"  Elicitation enabled: {next_section.elicit}")

    print("\n" + "=" * 80)
    print("✓ Integration demo complete!")
    print("\nKey takeaways:")
    print("- ✅ BMAD agents can be parsed and loaded")
    print("- ✅ System prompts are auto-generated from BMAD specifications")
    print("- ✅ BMAD tools (tasks, templates, elicitation) are available")
    print("- ✅ Session state can be maintained across workflow steps")
    print("- ✅ Ready for agent -> command -> task -> template -> elicitation workflows")
    print("\n💡 To create actual pydantic-ai agent:")
    print("   1. Set API key: export OPENAI_API_KEY=your-key")
    print("   2. Uncomment agent creation code")
    print("   3. Use agent.run() to interact with BMAD tools")


if __name__ == "__main__":
    # Note: This example requires API keys for the LLM
    # Set environment variables: OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.
    print("\n⚠️  Note: This is a demonstration script.")
    print("To run with actual LLM calls, ensure you have API keys configured.\n")

    # Run the demo
    asyncio.run(demo_workflow())

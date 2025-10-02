# BMAD Pydantic AI Integration - User Guide

## Overview

This integration layer bridges BMAD's markdown/YAML agent definitions with the [Pydantic AI](https://github.com/pydantic/pydantic-ai) framework, enabling you to operationalize BMAD personas, tasks, and templates as dynamic AI agents.

## Installation

```bash
cd pydantic-ai-integration
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

## Quick Start

### 1. Parse a BMAD Agent

```python
from bmad_pydantic_ai import BMADAgentParser

parser = BMADAgentParser()
agent_spec = parser.parse_agent_file("../bmad-core/agents/pm.md")

print(f"Agent: {agent_spec.agent.title}")
print(f"Role: {agent_spec.persona.role}")
print(f"Commands: {len(agent_spec.commands)}")
```

### 2. Generate System Prompt

```python
from bmad_pydantic_ai import SystemPromptComposer

composer = SystemPromptComposer()
system_prompt = composer.compose(agent_spec, include_commands=True)

# Use this prompt with any LLM framework
print(system_prompt)
```

### 3. Use with Pydantic AI

```python
from pydantic_ai import Agent
from bmad_pydantic_ai import BMADAgentParser, SystemPromptComposer

# Parse BMAD agent
parser = BMADAgentParser()
agent_spec = parser.parse_agent_file("../bmad-core/agents/pm.md")

# Generate system prompt
composer = SystemPromptComposer()
system_prompt = composer.compose(agent_spec)

# Create pydantic-ai agent
agent = Agent(
    "openai:gpt-4",
    system_prompt=system_prompt,
)

# Use the agent
result = await agent.run("Help me create a PRD")
```

## Core Components

### Models

Pydantic models representing BMAD structures:

- **`AgentSpec`**: Complete agent specification (persona, commands, dependencies)
- **`TaskSpec`**: Task definition with instructions and elicitation flags
- **`TemplateSpec`**: Template structure with sections and workflow config
- **`ElicitationSession`**: State for interactive elicitation workflows
- **`TemplateSession`**: State for template-driven document generation

### Parsers

Extract structured data from BMAD files:

- **`BMADAgentParser`**: Parse agent markdown files with YAML blocks
- **`BMADTaskParser`**: Parse task markdown files
- **`BMADTemplateParser`**: Parse YAML template files

### Tools

Operational tools for workflows:

- **`TaskRunner`**: Lazy-load and execute tasks
- **`TemplateDriver`**: Drive section-by-section document generation
- **`ElicitationEngine`**: Present numbered menus and apply elicitation methods

### Composers

- **`SystemPromptComposer`**: Generate system prompts from agent specs

### Registry

- **`AgentRegistry`**: Discover and manage agents from core and expansion packs
- **`ToolRegistry`**: Discover tasks, templates, and checklists

### State Management

- **`SessionManager`**: Track workflow state across multi-turn interactions

## Usage Examples

### Example 1: Parse and Display Agent

```python
from bmad_pydantic_ai import BMADAgentParser, SystemPromptComposer

parser = BMADAgentParser()
agent_spec = parser.parse_agent_file("../bmad-core/agents/pm.md")

print(f"✓ Agent: {agent_spec.agent.id}")
print(f"  Title: {agent_spec.agent.title}")
print(f"  Commands: {len(agent_spec.commands)}")

composer = SystemPromptComposer()
system_prompt = composer.compose(agent_spec)
print(f"\nSystem prompt: {len(system_prompt)} characters")
```

### Example 2: Parse Template

```python
from bmad_pydantic_ai import BMADTemplateParser

parser = BMADTemplateParser()
template = parser.parse_template_file("../bmad-core/templates/prd-tmpl.yaml")

print(f"Template: {template.template.name}")
print(f"Sections: {len(template.sections)}")
print(f"Workflow mode: {template.workflow.mode}")
```

### Example 3: Use Elicitation Engine

```python
from bmad_pydantic_ai import ElicitationEngine

engine = ElicitationEngine()

# Create session
session = engine.create_session(
    context="User requirements draft",
    content_type="technical"
)

# Show menu
menu = engine.format_menu(session)
print(menu)

# Apply method
result = engine.apply_method(session, "critique-refine", "content here")
print(result['prompt'])
```

### Example 4: Discover All Agents

```python
from bmad_pydantic_ai import AgentRegistry, ToolRegistry

# Discover agents
agent_registry = AgentRegistry("../")
agent_registry.discover_agents(include_expansion_packs=True)

agents = agent_registry.list_agents()
print(f"Found {len(agents)} agents")

# Discover tools
tool_registry = ToolRegistry("../")
tool_registry.discover_tools(include_expansion_packs=True)

tasks = tool_registry.list_tasks()
templates = tool_registry.list_templates()
print(f"Tasks: {len(tasks)}, Templates: {len(templates)}")
```

### Example 5: Complete Workflow

See `examples/example_05_complete_workflow.py` for a full demonstration of:

- Loading BMAD agent
- Creating pydantic-ai agent with BMAD system prompt
- Registering BMAD tools as agent tools
- Executing command -> task -> template -> elicitation workflow

## Architecture

### Context Minimization

Following BMAD principles, this integration respects context minimization:

- ✅ Files are loaded only when explicitly requested
- ✅ Dependencies are resolved lazily
- ✅ Templates and tasks are loaded on-demand
- ✅ No automatic pre-loading of resources

### Lazy Loading

All components use lazy loading:

```python
# TaskRunner loads tasks on-demand
runner = TaskRunner("../bmad-core")
task = runner.load_task("create-doc.md")  # Only loads when requested

# TemplateDriver loads templates on-demand
driver = TemplateDriver("../bmad-core")
template = driver.load_template("prd-tmpl.yaml")  # Only loads when needed
```

### Session State

Sessions maintain context across multi-turn workflows:

```python
from bmad_pydantic_ai import SessionManager

manager = SessionManager()
session = manager.create_session("session-123", "pm")

# Track template progress
manager.set_template_session(session_id, template_session)

# Track elicitation state
manager.set_elicitation_session(session_id, elicitation_session)

# Store variables
manager.set_variable(session_id, "project_name", "MyApp")
```

## Pydantic AI Integration

### Registering BMAD Tools

```python
from pydantic_ai import Agent, RunContext

agent = Agent("openai:gpt-4", deps_type=BMADDependencies)

@agent.tool
async def list_tasks(ctx: RunContext[BMADDependencies]) -> str:
    """List all available BMAD tasks."""
    return ctx.deps.task_runner.list_available_tasks()

@agent.tool
async def execute_task(ctx: RunContext[BMADDependencies], task_name: str) -> str:
    """Execute a BMAD task."""
    return ctx.deps.task_runner.get_task_instructions(task_name)
```

### Creating BMAD-Powered Agent

```python
async def create_bmad_agent(agent_id: str, root_path: str):
    # Parse BMAD agent
    parser = BMADAgentParser()
    agent_spec = parser.parse_agent_file(f"{root_path}/agents/{agent_id}.md")

    # Compose system prompt
    composer = SystemPromptComposer()
    system_prompt = composer.compose(agent_spec)

    # Create pydantic-ai agent
    agent = Agent(
        "openai:gpt-4",
        system_prompt=system_prompt,
        deps_type=BMADDependencies,
    )

    # Register tools
    register_bmad_tools(agent)

    return agent
```

## Supported BMAD Features

### ✅ Implemented

- Agent parsing (markdown with YAML)
- Persona extraction (role, principles, identity)
- Command parsing (name: description format)
- Dependency mapping (tasks, templates, checklists, data)
- Activation instructions
- System prompt generation
- Task lazy-loading
- Template parsing (recursive sections)
- Section-by-section generation
- Elicitation engine (9 methods + proceed)
- Session state management
- Agent/tool discovery
- Expansion pack support

### 🚧 Future Enhancements

- Template variable substitution
- Conditional section evaluation
- Multi-agent orchestration (round table, red/blue team)
- Command registry with automatic mapping
- Advanced elicitation prompts
- Template validation
- Agent behavior customization

## Best Practices

### 1. Respect BMAD Context Rules

```python
# ✅ Good - lazy load on demand
task = runner.load_task("create-doc.md")

# ❌ Bad - don't pre-load everything
for task in all_tasks:
    runner.load_task(task)
```

### 2. Use Session Management

```python
# Track state across workflow
manager = SessionManager()
session = manager.create_session(session_id, agent_id)
manager.add_command_to_history(session_id, "*create-prd")
```

### 3. Handle Elicitation Loops

```python
# Offer elicitation after content generation
if section.elicit:
    session = engine.create_session(content, "technical")
    menu = engine.format_menu(session)
    # Present menu to user, await selection
```

### 4. Compose Clear Prompts

```python
# Include commands for interactive use
system_prompt = composer.compose(agent_spec, include_commands=True)

# Exclude commands for fixed workflows
system_prompt = composer.compose(agent_spec, include_commands=False)
```

## Testing

Run the examples to verify functionality:

```bash
# Parse agent
python examples/example_01_parse_agent.py

# Parse template
python examples/example_02_parse_template.py

# Test elicitation
python examples/example_03_elicitation.py

# Discover agents/tools
python examples/example_04_discovery.py

# Complete workflow demo
python examples/example_05_complete_workflow.py
```

## Troubleshooting

### Import Errors

```bash
# Ensure package is installed in editable mode
pip install -e .
```

### Parser Errors

Check YAML format in agent files - some agents use mixed string/dict format for commands and instructions. The parser handles this automatically.

### API Key Issues

For pydantic-ai examples that use actual LLMs:

```bash
export OPENAI_API_KEY=your-key
export ANTHROPIC_API_KEY=your-key
```

## Contributing

To extend the integration:

1. Add new models in `bmad_pydantic_ai/models/`
2. Add parsers in `bmad_pydantic_ai/parsers/`
3. Add tools in `bmad_pydantic_ai/tools/`
4. Update examples to demonstrate new features

## License

This integration follows the same license as the BMAD-METHOD repository (MIT).

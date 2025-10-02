# BMAD Pydantic AI Integration

This package provides an integration layer between BMAD's markdown/YAML agent definitions and the Pydantic AI framework.

## Features

- **Agent Parser**: Extract structured data from BMAD agent markdown files
- **System Prompt Composer**: Generate system prompts from BMAD personas
- **Task Runner**: Lazy-load and execute BMAD tasks with elicitation support
- **Template Driver**: Parse YAML templates and enable section-by-section generation
- **Elicitation Engine**: Interactive numbered menus and multi-turn workflows
- **Session State**: Maintain context across agent interactions
- **Expansion Pack Discovery**: Auto-discover and register agents from expansion packs

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from bmad_pydantic_ai import BMADAgentParser, SystemPromptComposer

# Parse a BMAD agent
parser = BMADAgentParser()
agent_spec = parser.parse_agent_file("../bmad-core/agents/pm.md")

# Compose system prompt
composer = SystemPromptComposer()
system_prompt = composer.compose(agent_spec)

print(f"Agent: {agent_spec.agent.title}")
print(f"System prompt: {len(system_prompt)} characters")
```

### Use with Pydantic AI

```python
from pydantic_ai import Agent
from bmad_pydantic_ai import BMADAgentParser, SystemPromptComposer

# Parse BMAD agent and generate prompt
parser = BMADAgentParser()
agent_spec = parser.parse_agent_file("../bmad-core/agents/pm.md")

composer = SystemPromptComposer()
system_prompt = composer.compose(agent_spec)

# Create pydantic-ai agent
agent = Agent("openai:gpt-4", system_prompt=system_prompt)

# Use with BMAD workflows
result = await agent.run("Help me create a PRD")
```

## Documentation

- **[User Guide](GUIDE.md)**: Comprehensive documentation and examples
- **[Examples](examples/)**: Working code examples demonstrating all features

## Architecture

```
bmad_pydantic_ai/
├── models/          # Pydantic models for BMAD structures
├── parsers/         # Markdown and YAML parsers
├── composers/       # System prompt and content composers
├── tools/           # Task runner, template driver, elicitation engine
├── state/           # Session state management
└── registry/        # Agent and tool registry
```

## Examples

### 1. Parse Agent

```bash
python examples/example_01_parse_agent.py
```

Parse PM agent and display structured information.

### 2. Parse Template

```bash
python examples/example_02_parse_template.py
```

Parse PRD template and show section structure.

### 3. Elicitation Engine

```bash
python examples/example_03_elicitation.py
```

Demonstrate interactive elicitation with numbered menus.

### 4. Discovery

```bash
python examples/example_04_discovery.py
```

Discover all agents and tools in the repository.

### 5. Complete Workflow

```bash
python examples/example_05_complete_workflow.py
```

End-to-end demonstration of BMAD + Pydantic AI integration.

## Key Features

### Context Minimization

Following BMAD principles, this integration respects context minimization:

- Files are loaded only when explicitly requested
- Dependencies are resolved lazily
- Templates and tasks are loaded on-demand

### Elicitation Engine

Interactive numbered menus (0-9) for multi-turn workflows:

- Context-aware method selection
- Core methods: Expand/Contract, Critique, Identify Risks, Assess Alignment
- Technical methods: Tree of Thoughts, ReWOO, Meta-Prompting
- Collaborative methods: Agile Team, Stakeholder Roundtable, Red/Blue Team
- Creative methods: Innovation Tournament, Escape Room, Hindsight Reflection

### Template Driver

Section-by-section document generation:

- Recursive section parsing
- Conditional sections
- Variable substitution support
- Elicitation at section level
- Interactive workflow mode

### Registry

Auto-discovery of agents and tools:

- Scan bmad-core and expansion packs
- Register agents by role
- Discover tasks, templates, checklists
- Lazy-load on demand

## Testing

All examples run successfully:

```bash
# Run all examples
for example in examples/example_*.py; do
    echo "Running $example..."
    python "$example"
done
```

## Contributing

To extend the integration:

1. Add models in `bmad_pydantic_ai/models/`
2. Add parsers in `bmad_pydantic_ai/parsers/`
3. Add tools in `bmad_pydantic_ai/tools/`
4. Update examples to demonstrate features

## License

MIT (same as BMAD-METHOD)

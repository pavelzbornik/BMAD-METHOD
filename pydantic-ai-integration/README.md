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
agent_spec = parser.parse_agent_file("bmad-core/agents/pm.md")

# Compose system prompt
composer = SystemPromptComposer()
system_prompt = composer.compose(agent_spec)

# Use with pydantic-ai
# ... (coming soon)
```

## Architecture

- `models/`: Pydantic models for BMAD structures
- `parsers/`: Markdown and YAML parsers
- `composers/`: System prompt and content composers
- `tools/`: Task runner, template driver, elicitation engine
- `state/`: Session state management
- `registry/`: Agent and tool registry

## Context Minimization

Following BMAD principles, this integration respects context minimization:

- Files are loaded only when explicitly requested
- Dependencies are resolved lazily
- Templates and tasks are loaded on-demand

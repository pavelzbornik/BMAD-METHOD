```markdown
task:
  id: metric-inventory
  name: Metric Inventory
  description: Create a single-source inventory of product and experiment metrics, definitions and owners.
  persona_default: analytics-experimentation
  steps:
    - Export existing metric/metric-definition sources (dashboards, GA/GTM, analytics workspace, product docs).
    - For each metric record: id, canonical name, friendly name, formula, event/property mapping, owner, last validated date.
    - Tag metrics with business layer (North Star, Leading Input, Guardrail) and decision use-case.
    - Highlight instrumentation gaps and proposed fixes (event/property missing, ambiguous definitions).
    - Recommend canonical metric registry location and access controls.
  output: metric-inventory.md
```

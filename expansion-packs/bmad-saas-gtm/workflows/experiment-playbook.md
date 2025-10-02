# Experiment Playbook

This playbook outlines a lightweight experiment flow combining marketing, product and analytics.

1. Hypothesis
   - Define hypothesis, primary metric, and guardrail metrics.
2. Design
   - Create `growth-experiment-tmpl.yaml` using `templates/`.
3. Instrumentation
   - Map events using `data/sample-event-schema.md` and confirm with engineering.
4. Launch
   - Roll out using feature flags; track cohort in analytics.
5. Analyze
   - Use `retention-cohort-analysis.md` and `dashboard-specification.md` to report results.
6. Decide
   - Promote winner to backlog or iterate.

Artifacts produced:

- experiment-brief.md
- experiment-results.md
- dashboard-spec.json

Local artifacts (pack):

- artifacts/experiment-brief.md
- artifacts/experiment-results.md
- artifacts/experiments-log.md

# Product Launch Playbook

Purpose: coordinate marketing, product, analytics, and customer success for a staged SaaS product launch.

1. Preparation (2-4 weeks before launch)

   - Finalize positioning & messaging (`templates/messaging-framework-tmpl.yaml`).
   - Create launch checklist: announce channels, assets, and owner for each.
   - Confirm instrumentation: reference `data/sample-event-schema.md`.

2. Pre-Launch (1 week)

   - QA assets: landing page, email copy, social assets, docs.
   - Dry run with onboarding script (`tasks/onboarding-script-draft.md`).
   - Set up analytics dashboards (`tasks/dashboard-specification.md`).

3. Launch Day

   - Coordinate publish times and channels.
   - Monitor primary metrics and guardrails (errors, latency, signup success).
   - Customer success: standby for high-touch onboarding cases.

4. Post-Launch (1–4 weeks)

   - Analyze results, run cohort/retention checks (`tasks/retention-cohort-analysis.md`).
   - Collect qualitative feedback and update messaging.
   - Bake learnings into backlog and experiment hypotheses.

Artifacts:

- launch-plan.md
- messaging-deck.pdf
- launch-dashboard.json

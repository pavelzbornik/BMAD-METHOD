# BMAD SaaS Go-To-Market & Success Expansion Pack

This expansion pack adds non-technical personas focused on product success, growth, and retention for SaaS product teams.

## Personas Added

- Brand Strategist
- Product Marketing Manager
- Growth Marketer
- UX Copywriter
- SEO Strategist
- Customer Success Architect
- Analytics & Experimentation Specialist

## Design Principles

- Keep BMAD Core lean (no direct modifications to core agents)
- All outputs are structured via existing `create-doc.md` where possible
- Checklists enforce quality before handoff to technical teams
- Tasks are small, composable, single‑outcome procedures
- Elicitation (`elicit: true`) used on critical strategic sections (positioning, messaging, metrics)

## Recommended Workflow Integration

1. Brand & Messaging solidified BEFORE large-scale feature naming in PRD.
2. Positioning & ICP feed into PRD's “Target Users / Value Proposition” fields.
3. Growth & SEO artifacts inform backlog epics (acquisition engine, activation optimization).
4. Customer Success Journey informs onboarding feature priorities and story acceptance criteria.
5. Analytics event schema embedded early in Architecture doc to avoid retrofitting.
6. Experiment briefs become sharded stories for implementation (feature flags, tracking, reporting).

## Minimal Adoption Path

Start with:
- brand-strategist
- product-marketing-manager
- ux-copywriter
Then add:
- analytics-experimentation
- customer-success-architect
Finally layer in:
- seo-strategist
- growth-marketer

## Commands Mapping

All agents rely on existing `create-doc.md` + their custom templates/checklists.

## Adding to Your Project

1. Copy this expansion pack into `expansion-packs/bmad-saas-gtm/`
2. Ensure `create-doc.md` task is available (from core).
3. Activate persona via your orchestrator or directly in web context.
4. Use checklists before promoting artifacts to PRD or Architecture alignment passes.

---
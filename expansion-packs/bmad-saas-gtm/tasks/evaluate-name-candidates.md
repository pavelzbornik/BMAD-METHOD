<!-- Powered by BMAD™ Core -->
# ------------------------------------------------------------
# task: evaluate-name-candidates
# ------------------------------------------------------------
task:
  id: evaluate-name-candidates
  name: Evaluate Name Candidates
  description: Score and refine product/app name candidates
  persona_default: brand-strategist
  inputs:
    - names-list.md
  steps:
    - Collect evaluation criteria: memorability, differentiation, verbal flow, domain availability, trademark risk, semantic alignment.
    - Create scoring table (0–5 per criterion) with weighted total.
    - Highlight top 3. Provide rationale + risk notes.
    - Suggest refinement or mashups of close contenders.
    - Output updated ranked list.
  output: names-evaluation.md
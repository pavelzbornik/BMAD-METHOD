task:
  id: keyword-research
  name: Keyword Research
  description: Generate prioritized keyword universe by intent stage
  persona_default: seo-strategist
  steps:
    - Define intent buckets: Problem, Solution, Category, Brand, Comparison.
    - Generate seed list (internal + competitor SERP extraction if data provided).
    - Cluster semantically (topic groups).
    - Assign metrics placeholders (volume, difficulty, strategic value).
    - Recommend initial content cluster rollout sequence.
  output: keyword-universe.md
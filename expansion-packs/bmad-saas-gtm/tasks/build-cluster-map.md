task:
  id: build-cluster-map
  name: Build Content Cluster Map
  description: Map clusters → pillar & spokes with interlinking plan
  persona_default: seo-strategist
  steps:
    - Input: keyword-universe.md
    - Identify 5–8 pillar themes.
    - Assign spokes (supporting intent queries).
    - Define internal linking structure (pillar ↔ spokes, cross-cluster relevance).
    - Add schema/structured data opportunities per pillar.
  output: cluster-map.md
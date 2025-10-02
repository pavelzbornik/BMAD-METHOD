task:
  id: build-segmentation-matrix
  name: Build Segmentation Matrix
  description: Construct ICP segmentation and priority scoring
  persona_default: product-marketing-manager
  steps:
    - List hypothesized segments: industry, company size, role profile, maturity.
    - Define scoring criteria: TAM slice, urgency, budget alignment, competitive crowding, expansion potential.
    - Score and rank.
    - Output strategic focus rationale + deprioritized notes.
  output: segmentation-matrix.md
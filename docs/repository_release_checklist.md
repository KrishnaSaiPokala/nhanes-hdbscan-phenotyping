# Repository release checklist

Before tagging the public repository release:

- [ ] README headline results match the submitted manuscript.
- [ ] `preprint/medrxiv/v1/` contains the final manuscript and supplement PDFs.
- [ ] `figures/main/` contains final PNG/PDF/SVG figures.
- [ ] `tables/curated/` contains curated CSV/PDF tables.
- [ ] `results/summary/` contains the final aggregate results JSON.
- [ ] `docs/leakage_control.md` describes held-out variables.
- [ ] `docs/known_limitations.md` reflects manuscript limitations.
- [ ] `CITATION.cff` is updated after DOI assignment.
- [ ] CI passes.
- [ ] GitHub release tag created, recommended: `v1.0.0-preprint`.
- [ ] Optional: archive the release on Zenodo after final repository cleanup.

# Manuscript Results Scaffold

## Clustering solution and stability

The final discovery analysis included 6,048 adults and identified 3 non-noise HDBSCAN phenotypes plus an algorithmic noise/outlier group. Across final seeds, the mean pairwise ARI was 0.9935 and the mean pairwise NMI was 0.9885. The mean noise rate was 7.10%.

## Phenotype characterization

Phenotype -1 (Noise / outlier group) included 447 participants (7.4% of the analytic cohort). Top standardized drivers were: HDBSCAN noise label.
Phenotype 0 (Lipid-prediabetes metabolic-risk tendency) included 2,998 participants (49.6% of the analytic cohort). Top standardized drivers were: wbc z=-0.17; albumin z=-0.07; mean_sbp z=-0.06; mean_dbp z=-0.05.
Phenotype 1 (Lower-glycemic central-adiposity tendency) included 2,258 participants (37.3% of the analytic cohort). Top standardized drivers were: wbc z=0.20; albumin z=0.11; glucose z=-0.07; mean_dbp z=0.05.
Phenotype 2 (Smaller blood-pressure / renal-risk phenotype) included 345 participants (5.7% of the analytic cohort). Top standardized drivers were: mean_sbp z=0.18; wbc z=0.15; mean_dbp z=0.12; rdw z=0.12.

## Ablation robustness

Feature-block ablations evaluated whether the solution depended disproportionately on a single biomarker block. The exported ablation table reports cluster count, noise rate, silhouette, and ARI versus the full objective reference solution.

## Temporal replication

Best-match profile correlations in the pre-pandemic replication analysis ranged from 0.714 to 0.909, supporting partial temporal transportability of the phenotype structure.

## Interpretation boundary

This study should be interpreted as exploratory unsupervised phenotyping. Post-hoc enrichment is descriptive and should not be interpreted causally.

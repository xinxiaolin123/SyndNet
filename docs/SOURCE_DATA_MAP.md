# Aggregate reference results and controlled inputs

| Analysis | Controlled inputs | Public aggregate reference |
|---|---|---|
| Diagnostic performance | Case-level model predictions and fixed decisions | `results/reproduced_table2.csv`, `performance_ci.csv` |
| Ablations | Case-level ablation predictions | `results/reproduced_table3.csv`, `ablation_ci.csv`, `paired_effects.csv` |
| Fixed model benchmark | Case-level study model predictions | `results/reproduced_table4.csv`, `reproduced_bootstrap_ci.csv` |
| Supplementary discrimination | Case-level discrimination predictions | Aggregate-only rows in `results/supplementary_ci.csv` and `reproduced_supplementary_ci.csv` |
| Reader-study group analyses | Paired reader responses, approved assignments and locked predictions | `results/reader_study/` aggregate iMRMC, GLMM and publication tables |

Case-level records and individual-reader exports are not public source data in this revision. Public aggregate rows retain their frozen values. Input formats and access requirements are documented in DATA_ACCESS.md and reader_study_reproducibility/.

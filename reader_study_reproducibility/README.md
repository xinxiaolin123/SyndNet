# Reader-study reproducibility

This directory contains statistical scripts, methods, environment documentation and artificial input formats. Actual reader identifiers, assignments, responses and case-level records are controlled and are not distributed here. Public aggregate reference results are in `../results/reader_study/`.

Restore `environment/renv.lock` with the recorded R version. The complete pipeline implements structural checks, primary iMRMC, operating GLMMs, crossover specialty/experience analyses, exploratory safety GLMMs, individual-reader bootstrap intervals and publication outputs. Its statistical formulas and estimation rules are unchanged.

Store the approved input bundle in a separate controlled workspace with:

- `input/MRMC_REAL_READER_CASE_FINAL.csv`
- `input/MRMC_LOCKED_CASE_PREDICTIONS.csv`
- `input/reader_assignment.csv` containing the approved sequence lookup
- `qc/expected_auc_fingerprint.csv` containing the locked aggregate comparison values

The model-benchmark export also reads `reproduced_bootstrap_ci.csv` from the directory specified by `SYNDNET_REFERENCE_RESULTS_DIR`. From the repository root, after setting the environment variables for your shell:

```bash
export SYNDNET_READER_STUDY_ROOT=../controlled_reader_workspace
export SYNDNET_REFERENCE_RESULTS_DIR=../controlled_reference_results
Rscript --vanilla reader_study_reproducibility/R/run_all.R
```

PowerShell uses `$env:SYNDNET_READER_STUDY_ROOT='../controlled_reader_workspace'` and the analogous assignment for the reference directory. The runner requires an external workspace and writes generated inputs, per-reader outputs, fitted models, diagnostics and environment records there. These outputs must remain controlled. The example tables illustrate schema only and cannot reproduce the reported results.

The approved data request process is described in `../DATA_ACCESS.md`. Aggregate reference tables retain their frozen numeric values. Full statistical reproduction requires approved inputs; public-only checks cover syntax, metadata, hashes and artificial formats.

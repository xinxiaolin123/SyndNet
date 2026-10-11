# Reader study reproducibility

Run commands from the `MRMC` directory. Inputs are de-identified paired reader records, condition-level records, and recorded model predictions. Published statistics are supplied in `03_results`.

1. Restore the environment: install the recorded R version, install `renv`, and run `renv::restore(lockfile="05_environment/renv.lock")`. Exact versions appear in `05_environment/package_versions.csv` and `05_environment/sessionInfo.txt`.
2. Validate structural inputs with `02_R/00_input_qc.R`.
3. Run primary iMRMC inference with `02_R/01_primary_imrmc.R`.
4. Run operating-metric GLMMs with `02_R/02_operating_glmm.R`.
5. Run the secondary crossover GLMM with `02_R/03_secondary_glmm.R`.
6. Run the exploratory safety GLMM with `02_R/04_safety_glmm.R`.
7. Generate individual-reader bootstrap intervals with `02_R/reader_intervals.R`, then publication and figure-source CSVs with `02_R/05_publication_outputs.R`.
8. Compare reproducibility fingerprints after outputs have been generated with `02_R/06_reproducibility_checks.R`.

Execute the complete ordered pipeline with `Rscript --vanilla 02_R/run_all.R`. `SYNDNET_MRMC_ROOT` can specify the project directory. Expected fingerprints are used only in the final reproducibility step. Statistical models use structural inputs and observed outcomes.

Reader-averaged AUROCs and paired differences were analyzed using the iMRMC package, using U-statistic estimates with BDG variance and degrees-of-freedom inference. GLMMs use crossed reader and case random intercepts. Population-standardized marginal intervals use fixed-effect delta-method uncertainty conditional on fitted variance components. Individual-reader intervals use 10,000 paired reference-class-stratified case bootstrap resamples.

`MRMC_METHODS_FINAL_FACTS.md` specifies the design, model formulas, standardization, uncertainty assumptions, and software. `MRMC_RESULTS_FINAL_FACTS.md` is the numerical reference for manuscript writing. CSV exports retain full precision; publication tables apply display rounding.

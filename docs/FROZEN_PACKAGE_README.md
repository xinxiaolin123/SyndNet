# SyndNet scientific reproducibility

## Overview
Frozen derived predictions, scientific implementation, experiment records and statistical reproduction scripts. No model weights or raw radiographs are included.

## Included analyses
Table 2 diagnostic performance; Table 3 ablations and paired effects; Table 4 fixed SyndNet benchmark; primary and supplementary confidence-interval checks. Reader-averaged AUROCs and paired differences were analyzed using the iMRMC package, using U-statistic estimates with BDG variance and degrees-of-freedom inference. The reader analysis, formulas, environment, and ordered execution steps are provided in `MRMC/README.md`.

## Model configurations
Image-only baseline; Without residual; Matched residual; Residual-only; Final SyndNet; Permuted patient-specific correspondence; Parameter-matched shuffled anatomical support prior. The final model adds an internally fitted residual scale to frozen diagnostic, anatomical and reliability components.

## Experiment structure
Patient-level five-fold cross-validation. Inference-only controls share their trained components. Seed repetitions are not independent clinical samples. Selection rules in the supplied implementation retain their original numerical thresholds; identifiers ending in noninferiority_check name selection criteria, not a new inferential test.

## Seeds and folds
Seeds: 42, 123, 456. Folds: 0, 1, 2, 3, 4.

## External validation
The four external validation centers were held out from model training, hyperparameter tuning, model selection, threshold selection and calibration.
No external refitting or recalibration was performed.

## Threshold policy
Internal diagnostic results inherit outer-fold thresholds. External diagnostic results use one internally derived global threshold. The reader-study model benchmark retains its separately prespecified global operating policy. Reproduction uses stored fixed predictions and never selects thresholds.

## Reproducing Table 2
From the package root: `python scripts/reproduce_table2.py`.

## Reproducing Table 3
`python scripts/reproduce_table3.py`.
Marginal metrics are means of seed-specific metrics. Paired AUROC effects use seed-averaged probabilities; they are not differences between marginal means.

## Reproducing Table 4 model benchmark
`python scripts/reproduce_table4_model_benchmark.py`.
The model is a fixed benchmark, not a random-reader arm.

## Reproducing bootstrap CI
`python scripts/reproduce_bootstrap_ci.py`.
`python scripts/reproduce_supplementary_ci.py`. Individual-reader intervals are imported from `MRMC/03_results/reader_paired_bootstrap.csv`; regenerate them using the R reader pipeline before this aggregate export.
Patient samples are shared across seeds and paired models. Internal strata are fold × reference class; pooled external strata are center × reference class. The matched-residual comparison retains its original reference-class-stratified stream. Center 3 sensitivity retains its existing Wilson interval at 19/19 successes. Calibration retains its existing intervals. Individual-reader intervals are conditional case-bootstrap summaries, not replacements for iMRMC inference.
For safety and specialty analyses, values are population-standardized marginal accuracies from the crossover-adjusted model; confidence intervals and P values refer to the adjusted within-stratum assistance contrast.

## Environment
Install `requirements.txt`; `environment.yml` provides a conda environment specification. Statistical reproduction requires only included derived data. Model training additionally requires author-supplied images, input manifests and frozen starting checkpoints. No training is required for these reproduction commands. For scientific implementation entry points, add `code/models` and `code/utils` to PYTHONPATH. Scalar fitting uses caller-supplied SYNDNET_CONFIG and SYNDNET_WORK_DIR. Residual-scaling selection and evaluation inputs use RESIDUAL_SCALING_SELECTION.json and RESIDUAL_SCALING_EVALUATION.csv.

## Data fields
Release-specific de-identified case codes; reference labels; probabilities; fixed predictions; model, seed, fold and cohort. `data/final_model_predictions.csv` supports Table 2; `data/ablation_patient_predictions.csv` supports Table 3; `data/reader_study_model_predictions.csv` supports the fixed model benchmark. `results/experiment_manifest.csv` identifies component availability. Training records are provided only where recorded; unrecorded series are not inferred.

## Expected outputs
`results/reproduced_table2.csv`, `results/reproduced_table3.csv`, `results/reproduced_table4.csv`, `results/reproduced_bootstrap_ci.csv`, `results/reproduced_supplementary_ci.csv`. Point estimates and intervals are checked at absolute tolerance 1e-10. Reference estimates and intervals are in configs/expected_points.json, results/ablation_ci.csv, results/paired_effects.csv and results/supplementary_ci.csv. SHA256SUMS.txt covers the release files.

Text outputs use UTF-8 encoding with LF line endings to ensure deterministic cross-platform reproduction.

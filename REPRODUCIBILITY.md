# Reproducibility

## Scientific authority and preservation

The repository derives from the permanently frozen submission archive with SHA256 `da559b37913fd0ce829557d4e5fac9abfe218405f89748de7b665f6a8edc9eb7`. `environments/frozen_payload_manifest.json` records the original payload hashes. Scientific code, configurations, inputs and numerical outputs are copied byte-for-byte. The original root README is retained as `docs/FROZEN_PACKAGE_README.md`; the original SHA256 manifest is retained as `FROZEN_PACKAGE_SHA256SUMS.txt`. Added release documentation and validation scripts do not refit models or change statistical results.

## Python numerical analyses

Use Python 3.12 and `environments/analysis-verified.txt` for the separately verified numerical environment. The supplied `requirements.txt` and `environment.yml` are retained unchanged; they contain version ranges rather than a historical exact Python lock. The new verification lock is not claimed to reconstruct an unrecorded training environment.

From the repository root:

```bash
python scripts/validate_release.py
python -m unittest discover -s tests
python scripts/reproduce_table2.py
python scripts/reproduce_table3.py
python scripts/reproduce_table4_model_benchmark.py
python scripts/reproduce_bootstrap_ci.py
python scripts/reproduce_supplementary_ci.py
```

The supplementary exporter reads final individual-reader intervals from `MRMC/03_results/reader_paired_bootstrap.csv`. To regenerate those intervals, run the R reader pipeline first. The fixed model benchmark uses recorded predictions and does not choose a new threshold. Original Python statistical implementations are unchanged. Reproduction overwrites numerical output files; run it in a separate copy.

## R reader study

The actual clean-analysis R version and package versions are recorded in `MRMC/05_environment/sessionInfo.txt`, `package_versions.csv`, and `renv.lock`. Install the recorded R version, then restore the lock from the `MRMC` directory:

```r
install.packages("renv")
renv::restore(lockfile = "05_environment/renv.lock")
```

Then, from `MRMC`:

```bash
Rscript --vanilla 02_R/run_all.R
```

The supplied runner executes: structural input QC → primary iMRMC → operating GLMMs → secondary crossover GLMM → exploratory safety GLMM → individual-reader intervals → publication/figure outputs → post-analysis fingerprint QC. Expected AUROC fingerprints are not prerequisites for fitting models. No reader score, binary decision, or model prediction is regenerated or optimized.

Reader-averaged AUROCs use iMRMC U-statistic estimates with BDG variance and degrees-of-freedom inference. GLMM marginal intervals use fixed-effect delta-method uncertainty conditional on fitted variance components; they do not propagate variance-component uncertainty. Individual-reader AUROC intervals use 10,000 paired reference-class-stratified case bootstrap resamples. Details and exact frozen results are in the MRMC facts documents.

## Scope, installation and runtime

Numerical Python reproduction requires only released derived data. R GLMM and bootstrap calculations require more time than point-metric commands. The verification report records measured elapsed times on the validation machine; these are not universal runtime guarantees. No GPU is required for released numerical analyses. Installation duration depends on package availability and hardware and was not measured as a clean historical environment restoration.

Version 1.1.0 adds verified inference checkpoints and an isolated fresh-environment paired-image test. CUDA float16 inference is supported in the documented environment; CPU fidelity and complete public retraining are not established.

## Verification

`docs/VALIDATION_REPORT.json` distinguishes checks actually run from checks supported by retained frozen outputs. Integrity tests cover every frozen payload file, R QC statuses, paired record counts, and the official unmodified license. Full R refitting is not part of this repository-construction pass; the original clean-R results and actual environment are preserved. Exact manuscript-text concordance remains unverified because no manuscript was supplied.

## Inference verification (v1.1.0)

Checkpoint manifest SHA256: `826333f9ab894b89c2c9d14501bbf3208256a586869ad05ec0b561211afcc953`. Weight archive SHA256: `160aa8f1e976d9aea65bd344dea90b331753aee394e70f453af2f4cae40b02e9`. Install `environments/inference-verified.txt`, run `python scripts/download_weights.py --output-dir downloaded_weights`, then:

```bash
python scripts/infer_pair.py --ap path/to/AP.png --lat path/to/LAT.png --weights-dir downloaded_weights/weights --output prediction.json
```

All 15 full model states load strictly without missing or unexpected keys. The 90-case locked fidelity sample covers all five internal folds and four external centres with both labels; maximum absolute difference is 5.96e-8, with zero decision mismatches. This is not a full 2050-case rerun. A separate 40-case single-pair audit verifies the published batch-size-4 rule. The initial different-batch attempt failed the same tolerance; its findings and original-batch replay are disclosed. Full retraining requires controlled-access data, annotations and manifests. Domain-specific SSL initialization is training-only once complete diagnostic states are supplied. Detailed hardware, versions, scope and measured runtime are in `docs/CHECKPOINT_FIDELITY_REPORT.json` and `docs/INFERENCE_SMOKE_TEST.json`.

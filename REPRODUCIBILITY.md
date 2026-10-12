# Reproducibility

## Public execution checks

Use Python 3.12 and `environments/analysis-verified.txt`:

```bash
python -m pip install -r environments/analysis-verified.txt
python scripts/validate_release.py
python -m unittest discover -s tests
python scripts/validate_synthetic_formats.py
python examples/demo_metrics.py
```

These checks cover source integrity, checkpoint metadata, imports and artificial input formats. Synthetic examples do not reproduce study statistics or demonstrate diagnostic accuracy. The current public tree excludes all case-level predictions and actual reader records.

## Numerical analyses with controlled inputs

Request approved derived inputs through DATA_ACCESS.md and keep them outside this repository. Set `SYNDNET_ANALYSIS_DATA_DIR` to the approved directory containing `final_model_predictions.csv`, `ablation_patient_predictions.csv`, `reader_study_model_predictions.csv` and `supplementary_discrimination_predictions.csv`. From the repository root:

```bash
python scripts/reproduce_table2.py
python scripts/reproduce_table3.py
python scripts/reproduce_table4_model_benchmark.py
python scripts/reproduce_bootstrap_ci.py
```

Outputs default to the Git-ignored `reproduction_output/` directory. Fixed predictions, thresholds, bootstrap estimands and computation are unchanged. Aggregate reference CSVs remain in `results/`. For supplementary reader intervals, also set `SYNDNET_ANALYSIS_REFERENCE_DIR` to the controlled original reference directory, `SYNDNET_READER_RESULTS_DIR` to the approved reader-study results and `SYNDNET_ANALYSIS_OUTPUT_DIR` to an external controlled output directory before `python scripts/reproduce_supplementary_ci.py`. Per-reader outputs must remain controlled.

## Reader study

Restore `reader_study_reproducibility/environment/renv.lock` using the recorded R 4.6.1 environment. See the directory README for the approved paired records, locked predictions, separate assignment table and aggregate reference fingerprint required in an external controlled workspace. Configure `SYNDNET_READER_STUDY_ROOT` and `SYNDNET_REFERENCE_RESULTS_DIR`, then:

```bash
Rscript --vanilla reader_study_reproducibility/R/run_all.R
```

The runner refuses an absent or in-repository controlled workspace. It performs the complete iMRMC, operating/crossover/safety GLMM and reader-bootstrap analyses, writing private outputs externally. Statistical formulas, fixed-effect delta-method uncertainty conditional on fitted variance components, and 10,000 paired reference-class-stratified reader bootstrap resamples are unchanged. Public synthetic formats are documentation, not substitutes for study inputs.

## Frozen inference

Use a separate Python 3.12 environment with `environments/inference-verified.txt`, download final checkpoints, and run:

```bash
python scripts/download_weights.py --output-dir downloaded_weights
python scripts/infer_pair.py --ap path/to/AP.png --lat path/to/LAT.png --weights-dir downloaded_weights/weights --output prediction.json
```

Weights comprise five diagnostic, five anatomy, five reliability and fifteen residual states. Individual SHA256 values are listed in `weights/README.md` and `MANIFEST.json`. The existing immutable published archive remains the download source; a clean local weight archive is prepared separately for review. No intermediate checkpoints, optimizer states or training snapshots are in the current source tree.

Inference was verified with Windows 11, Python 3.12.14, PyTorch 2.14.0+cu132, torchvision 0.29.0+cu132 and CUDA 13.2 on an RTX 5090 D v2. CPU fidelity and other-platform equivalence are unestablished. CUDA float16 output depends on batch context: the paired adapter uses four replicated pairs. Original size-12 internal and final partial external batch contexts are needed for frozen-probability fidelity. Full-cohort comparisons found zero locked-threshold decision changes but probability differences up to 0.007227 under alternative contexts. See docs/INFERENCE_VALIDATION.md.

Full retraining requires controlled images, annotations and manifests. No scientific model, checkpoint tensors, residual scales, operating thresholds or reference aggregate estimates were changed during privacy cleanup.

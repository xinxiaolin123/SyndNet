# SyndNet

SyndNet is an anatomy-aware deep learning framework for predicting ankle syndesmotic mechanical stability from paired preoperative anteroposterior (AP) and lateral radiographs. It combines a diagnostic image representation with probabilistic anatomical anchors, reliability weighting and an anatomy-aligned residual. The repository provides the scientific implementation, aggregate reference results, statistical analyses, synthetic input formats and frozen inference checkpoints. The reference target is mechanical stability established by the study reference assessment. Radiographic phenotype proxies describe image patterns; they are not direct measurements of biomechanical stress, strain or force.

## Model overview

An anatomy teacher estimates probabilistic distributions for eight anatomical anchors: five in the AP view and three in the lateral view. A diagnostic pathway supplies image features. Anatomy-guided soft pooling aligns local feature summaries with the anchor distributions. Reliability weighting incorporates visibility, uncertainty and image-quality information. A fixed anatomical support matrix connects anchors to radiographic proxy phenotypes. The final logit combines the diagnostic baseline with the anatomy-aligned residual using an internally fitted scale.

Frozen inference uses three seeds, 42, 123 and 456, and five folds per seed. For a new examination, five fold logits are averaged within each seed, transformed to probabilities, and then averaged across the three seeds. The locked global operating threshold is `0.012530357984719657`; a prediction of 1 denotes mechanical instability. Averaging all fifteen probabilities directly would implement a different aggregation rule. Residual scales, support buffers and the threshold are supplied with the checkpoints.

## Study and validation

The study includes an auxiliary normal-anatomy cohort, an internal development cohort and four external validation cohorts. The study diagnostic evaluation comprises 1,461 internal cases and 589 external cases, for 2,050 cases in total. Internal predictions follow prespecified held-out-fold evaluation; external predictions use the five-fold ensemble within each seed. These distinct evaluation paths are retained in numerical analyses; the case-level inputs are controlled.

The crossover reader study includes 15 readers and 2,050 cases, yielding 30,750 paired reader-case observations and 61,500 condition-level records. Analyses compare unaided and AI-assisted interpretation. The R pipeline implements primary multireader multicase AUROC inference, operating-metric mixed models, crossover analyses, specialty and experience analyses, exploratory safety analyses, and individual-reader bootstrap intervals. Methods and reference results are documented in `reader_study_reproducibility/`. Interpretation of performance should follow the study populations, reference assessment and uncertainty estimates.

## Repository structure

| Directory | Contents |
|---|---|
| `code/` | Models, training and evaluation entry points, image utilities and bootstrap implementation |
| `configs/` | Configurations, folds, seeds, scales, thresholds and numerical references |
| `data/` | Synthetic examples and input-format documentation |
| `scripts/` | Numerical reproduction, checkpoint download and paired-image inference |
| `inference/` | Checkpoint reconstruction, preprocessing and ensemble execution |
| `reader_study_reproducibility/` | Statistical scripts, methods, synthetic formats and environment documentation |
| `results/` | Main and supplementary numerical source tables |
| `weights/` | Checkpoint hashes, configuration and component relationships |
| `environments/` | Verified analysis and inference dependency specifications |
| `examples/` | Nonclinical metric and image-input examples |
| `docs/` | Source-data mapping, inference methods and validation evidence |
| `tests/` | Lightweight numerical and integrity checks |

Checkpoint tensors are distributed separately as a GitHub Release asset. Numerical reproduction requires approved derived predictions stored outside the repository, but does not require inference weights. `docs/SOURCE_DATA_MAP.md` identifies inputs and corresponding source tables. Full-precision CSVs support comparisons with reproduced outputs; manuscript display rounding should be applied separately.

## Reproduce numerical analyses

Use Python 3.12 in a dedicated environment. From the repository root:

```bash
python -m venv .venv
# Activate the environment for your operating system.
python -m pip install -r environments/analysis-verified.txt
python scripts/validate_release.py
python -m unittest discover -s tests
python scripts/validate_synthetic_formats.py
python examples/demo_metrics.py
```

These public-only commands check integrity and artificial formats; they do not reproduce publication statistics. Actual case-level predictions and reader records are controlled. After approved access, set `SYNDNET_ANALYSIS_DATA_DIR` to an external input directory, then run `scripts/reproduce_table2.py`, `scripts/reproduce_table3.py`, `scripts/reproduce_table4_model_benchmark.py` and the bootstrap commands in [reproducibility](REPRODUCIBILITY.md). The calculations retain fixed decisions, operating thresholds and estimands. Outputs default to the Git-ignored `reproduction_output/` directory. Aggregate reference CSVs remain public for numerical comparison.

For the complete reader analysis, restore `reader_study_reproducibility/environment/renv.lock` with the recorded R version. Configure `SYNDNET_READER_STUDY_ROOT` and `SYNDNET_REFERENCE_RESULTS_DIR` for approved external inputs, then run `Rscript --vanilla reader_study_reproducibility/R/run_all.R` from the repository root. The runner refuses an in-repository controlled workspace and writes confidential outputs externally. It fits statistical models, computes individual-reader intervals and exports publication tables. Primary AUROC inference uses iMRMC U-statistic estimates with BDG variance and degrees-of-freedom inference. GLMM marginal intervals condition on fitted variance components; individual-reader intervals use 10,000 paired, reference-class-stratified case resamples. Details appear in [statistical methods](reader_study_reproducibility/STATISTICAL_METHODS.md).

## Run paired-image inference

Use a separate Python 3.12 inference environment with the documented CUDA configuration:

```bash
python -m pip install -r environments/inference-verified.txt
python scripts/download_weights.py --output-dir downloaded_weights
python scripts/infer_pair.py --ap path/to/AP.png --lat path/to/LAT.png --weights-dir downloaded_weights/weights --output prediction.json
```

The downloader verifies the published archive before extraction. Individual file hashes and tensor hashes are recorded in `weights/MANIFEST.json`. Output records the probability, threshold and binary prediction. State files require approximately 924 MB extracted; the compressed archive is approximately 859 MB. Execution and installation time depend on hardware and package availability.

Inputs are paired preoperative AP and lateral ankle radiographs. Deterministic preprocessing converts each image to grayscale, crops the defined border, pads to a square, resizes to 384 × 384, repeats the grayscale channel and applies ImageNet normalization. Orientation, view selection and acquisition conventions must match study inputs. The command does not perform DICOM windowing or orientation canonicalization. See [preprocessing](docs/INFERENCE_PREPROCESSING.md) and [inference specification](docs/FINAL_INFERENCE_SPECIFICATION.md).

For an execution example, run `python examples/make_synthetic_pair.py --output-dir synthetic`, then supply `synthetic/AP.png` and `synthetic/LAT.png` to the same inference command. These nonclinical patterns and their predictions have no diagnostic meaning.

## Reproducibility scope

1. **Numerical analyses:** statistical code and aggregate reference values are public; full reproduction requires approved controlled predictions and reader records. Public checks use artificial formats only.
2. **Frozen inference:** released states support paired-image inference in the validated CUDA float16 environment. Numerical fidelity is sensitive to batch context; the single-pair adapter evaluates four replicated pairs and returns the first result. Internal out-of-fold reproduction requires its original batch context and fold-specific evaluation. Evidence is in [inference validation](docs/INFERENCE_VALIDATION.md).
3. **Full retraining:** controlled radiographs, annotations and study manifests are required. Trained diagnostic states include encoder and prototype buffers, so separate training initialization is unnecessary for frozen inference.

CPU fidelity and transfer to other computational platforms have not been established. Clinical scope concerns fracture-associated paired preoperative examinations. Isolated ligament injuries, postoperative imaging or alternative projections require separate validation. Model advice does not replace intraoperative mechanical assessment; incorrect advice can impair reader decisions. [MODEL_CARD.md](MODEL_CARD.md) describes these limitations.

Full-cohort comparison found no locked-threshold decision changes across 2,050 cases. Original-context replay reproduced frozen probabilities to approximately `1.11e-16`; changing execution context produced larger probability differences, up to `0.007227` for replicated-pair versus frozen evaluation. This decision agreement does not imply that arbitrary batch contexts reproduce the same probabilities. The original final partial external batch also requires its original context for numerical fidelity.

## Data availability

The current public tree contains aggregate tables and synthetic examples. Case-level predictions, actual reader responses and assignments are controlled. Requests for de-identified controlled data should be sent to Xinxiao Lin at **2060753088@qq.com**, with applicant and institutional details, research purpose, requested data and a data-management plan. Ethics approval or exemption is required where applicable. Requests normally receive an initial response within 30 days and undergo scientific, privacy and institutional review. Approved use is limited to the agreed research purpose; re-identification and unauthorized redistribution are prohibited. Approval and access to the complete raw dataset are not guaranteed. See [DATA_ACCESS.md](DATA_ACCESS.md).

## Citation

Please cite **Xinxiao Lin, SyndNet, version 1.1.1**, and the [software repository](https://github.com/xinxiaolin123/SyndNet). Structured metadata, including the author's ORCID, are provided in [CITATION.cff](CITATION.cff).

## Licence

Project code and authored model states are distributed under the standard [Apache License 2.0](LICENSE), Copyright 2026 SyndNet authors. Dependencies retain their respective licences; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Controlled-data conditions are described separately in the data availability statement.

# SyndNet

**An anatomy-aware deep learning framework for predicting ankle syndesmotic mechanical stability from paired preoperative radiographs**

SyndNet uses paired anteroposterior (AP) and lateral ankle radiographs to predict mechanical stability of the distal tibiofibular syndesmosis. Probabilistic anatomical anchors guide integration with a diagnostic feature representation through anatomy-aligned pooling, anchor reliability, and a residual pathway. This repository provides the scientific implementation and released numerical analyses for research; radiographic phenotype proxies are not direct measurements of biomechanical stress, strain, or force.

## Overview

1. An anatomy teacher produces probabilistic anchor distributions.
2. Eight anchors comprise five AP and three lateral anchors.
3. A diagnostic pathway supplies image feature representations.
4. Anatomy-guided soft pooling aligns local feature summaries with anchor distributions.
5. Anchor reliability incorporates visibility, uncertainty, and image-quality information.
6. The anatomy-aligned residual uses radiographic proxy phenotypes.
7. The final model combines the diagnostic logit and an internally fitted residual scale.

Implementation entry points are in `code/models/anatomy_model.py`, `diagnostic_model.py`, `reliability_model.py`, `matched_residual_model.py`, and `final_syndnet.py`. Original filenames and imports are preserved.

## Study scope

The study distinguishes an auxiliary normal-anatomy cohort, an internal development cohort, four external validation cohorts, and an MRMC reader study. Raw images for these cohorts are not released here. The frozen reader analysis comprises 15 readers, 2,050 cases, 30,750 paired reader-case records, and 61,500 condition-level records. Further design and statistical details are in [MRMC methods](MRMC/MRMC_METHODS_FINAL_FACTS.md); cohort counts not established by the released derived files are not inferred.

## Repository contents

| Directory | Purpose |
|-----------|---------|
| `code/models/`, `code/training/`, `code/evaluation/`, `code/utils/` | Scientific implementation and original training/evaluation entry points |
| `code/bootstrap/` | Shared numerical bootstrap implementation |
| `configs/` | Frozen configurations, thresholds, folds, seeds, and reference outputs |
| `scripts/` | Python numerical reproduction and release validation |
| `data/` | Approved de-identified frozen predictions and reader scores |
| `results/` | Frozen main/supplementary numerical outputs |
| `MRMC/` | Clean reader inputs, R statistical scripts, publication CSVs, QC, and actual environment lock |
| `environments/` | Verified numerical-analysis environment and dependency guidance |
| `third_party/` | Separate upstream license records and available license texts |
| `tests/` | Lightweight integrity/reproduction tests |
| `docs/` | Methods, source-data mapping, archival instructions, and retained package documentation |

The original flat implementation organization is retained rather than converted into an unverified installable Python package. Source-data CSVs are in `results/` and `MRMC/03_results/`; the authoritative archive contains no submission XLSX workbook.

## Reproducibility levels

### Level 1 — Numerical-result reproduction

Released derived predictions support diagnostic metrics, ablations, the fixed SyndNet reader-study benchmark, and bootstrap analyses. De-identified reader inputs and the R pipeline support primary iMRMC, operating-metric GLMMs, secondary crossover and exploratory safety analyses, and individual-reader bootstrap intervals. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for execution order, environment assumptions, validation results, and limitations.

### Level 2 — Inference reproduction

Publicly reproducible using the released frozen inference checkpoints and locked preprocessing/inference pipeline. Version 1.1.0 adds a lossless Release weight asset and a verified paired-image command. Supported verification environment: Python 3.12, PyTorch 2.14.0+cu132, torchvision 0.29.0+cu132, CUDA GPU; CPU fidelity is not established. [Fidelity report](docs/CHECKPOINT_FIDELITY_REPORT.md), [single-pair context audit](docs/SINGLE_PAIR_CONTEXT_AUDIT.json), and [clean-environment smoke test](docs/INFERENCE_SMOKE_TEST.json) describe the checks and batch-size sensitivity.

### Level 3 — Full model retraining

Requires controlled-access radiographs, annotations and study manifests and is therefore not fully reproducible from public materials alone. The trained diagnostic states include their encoder and prototype buffers; domain-specific SSL initialization is not an additional inference dependency.

## Quick start

```bash
git clone https://github.com/xinxiaolin123/SyndNet.git
cd SyndNet
python -m venv .venv
# Activate the environment using the command appropriate to your operating system.
python -m pip install -r environments/analysis-verified.txt
python scripts/validate_release.py
python scripts/reproduce_table2.py
python scripts/reproduce_table3.py
python scripts/reproduce_table4_model_benchmark.py
```

These commands reproduce numerical results from stored predictions; no model training or imaging checkpoint is required. Full bootstrap and R commands are documented in [REPRODUCIBILITY.md](REPRODUCIBILITY.md). Reproduction scripts write output CSVs; use a separate working copy when preserving the original frozen payload.

## Data and code access

See [DATA_ACCESS.md](DATA_ACCESS.md) and [CODE_AVAILABILITY.md](CODE_AVAILABILITY.md). The clinical reference target is mechanical stability; radiographic proxy phenotypes should not be described as direct biomechanical measurements. Exact correspondence with manuscript text must be checked against the submitted manuscript, which is not part of the archive.

## License and citation

Copyright 2026 SyndNet authors. Project code is licensed under the unmodified [Apache License 2.0](LICENSE). Third-party software retains its own licenses; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Research-purpose statements do not add restrictions to the license.

Citation metadata is in [CITATION.cff](CITATION.cff). The collective credit is supplied; individual author names, affiliations, funding and article identifiers have not been invented. Archival DOI: **DOI_PENDING**. GitHub provides versioned access but does not itself establish DOI-based archival permanence; see [archival instructions](docs/ARCHIVING.md).

## Paired-image inference (v1.1.0)

Use a separate Python 3.12 environment for inference; it is independent of the numerical-analysis environment.

```bash
python -m venv .venv
# Activate the environment for your operating system.
python -m pip install -r environments/inference-verified.txt
python scripts/download_weights.py --output-dir downloaded_weights
python scripts/infer_pair.py --ap path/to/AP.png --lat path/to/LAT.png --weights-dir downloaded_weights/weights --output prediction.json
```

For a nonclinical plumbing test, generate patterns with `python examples/make_synthetic_pair.py --output-dir synthetic`, then supply `synthetic/AP.png` and `synthetic/LAT.png` to the same command. Synthetic predictions have no diagnostic meaning. Installation requires approximately 2 GB for the PyTorch wheel download plus the extracted environment; weights require approximately 924 MB uncompressed. Inference runtime is recorded in the smoke report and varies by hardware.

The single-pair adapter preserves the original external batch-size-4 CUDA kernel context using four identical copies and returns the first prediction. Full clinical scope, image conventions, aggregation and numerical sensitivity are documented in [MODEL_CARD.md](MODEL_CARD.md), [preprocessing](docs/INFERENCE_PREPROCESSING.md), and [final specification](docs/FINAL_INFERENCE_SPECIFICATION.md). The v1.0.0 tag and Release remain immutable; all frozen numerical outputs are unchanged.

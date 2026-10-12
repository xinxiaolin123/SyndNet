# SyndNet

SyndNet is an anatomy-informed deep learning framework for research on ankle syndesmotic mechanical stability using paired anteroposterior (AP) and lateral radiographs. This repository provides public software implementation accompanying the study: inference code, released checkpoint interfaces and synthetic examples. It does not provide clinical study records or manuscript result tables.

## Installation

Use Python 3.12 in a dedicated environment:

```bash
python -m venv .venv
# Activate the environment for your operating system.
python -m pip install -r environments/inference-verified.txt
```

The inference environment was verified with CUDA on an NVIDIA GPU. CPU and other-platform numerical fidelity have not been established. See [environment notes](environments/README.md).

## Checkpoints and inference

```bash
python scripts/download_weights.py --output-dir downloaded_weights
python scripts/infer_pair.py --ap path/to/AP.png --lat path/to/LAT.png --weights-dir downloaded_weights/weights --output prediction.json
```

Released checkpoints are provided for inference. Use the supplied configuration for reproducible execution. Checkpoint names, purposes and SHA256 hashes are listed in [weights/README.md](weights/README.md).

Supply correctly oriented, exported AP/lateral images. The adapter performs deterministic grayscale conversion, border cropping, square padding, resizing and normalization; it does not perform DICOM conversion or automatic orientation correction. See [preprocessing](docs/INFERENCE_PREPROCESSING.md). Output contains a probability, the supplied operating parameter and a binary model prediction. Predictions are research outputs and do not replace clinical assessment.

For a nonclinical execution example:

```bash
python examples/make_synthetic_pair.py --output-dir synthetic
python scripts/infer_pair.py --ap synthetic/AP.png --lat synthetic/LAT.png --weights-dir downloaded_weights/weights --output synthetic_prediction.json
```

Synthetic images and outputs have no diagnostic meaning.

## Public checks

```bash
python -m pip install -r environments/analysis-verified.txt
python scripts/validate_release.py
python -m unittest discover -s tests
python scripts/validate_synthetic_formats.py
python examples/demo_metrics.py
```

These commands check software integrity and artificial formats, not study performance. [REPRODUCIBILITY.md](REPRODUCIBILITY.md) describes the public scope. The [reader-study directory](reader_study_reproducibility/README.md) provides an input framework and synthetic formats without confidential records or study-specific statistical specifications.

## Data availability

Raw radiographs and associated clinical records are not publicly available because of ethics approval and institutional data-governance requirements. Requests for de-identified controlled data should be directed to **2060753088@qq.com** with applicant identity, institutional affiliation, research purpose, requested data elements and a data-management plan. Requests undergo scientific, privacy and institutional review. Requests will normally receive an initial response within 30 days. This is an initial acknowledgement or review response, not a guarantee of approval or data release within 30 days. See [DATA_ACCESS.md](DATA_ACCESS.md) for conditions.

## Citation and licence

Cite Xinxiao Lin, SyndNet, version 1.1.1, using [CITATION.cff](CITATION.cff). Project software is licensed under the standard [Apache License 2.0](LICENSE), Copyright 2026 SyndNet authors. Dependencies retain their licences; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

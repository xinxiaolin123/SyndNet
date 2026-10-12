# Data input formats

This directory contains synthetic examples and format documentation only. Study radiographs, clinical spreadsheets, case-level predictions, reader responses and study manifests are controlled inputs and are not included in the current public tree.

`example_manifest.csv` describes a nonclinical AP/lateral pair. Generate its patterns from the repository root with `python examples/make_synthetic_pair.py --output-dir data/synthetic_examples`. The patterns have no diagnostic meaning. `synthetic_examples/metric_predictions.csv` contains four artificial observations for checking the numerical interface, not study results.

Approved numerical inputs should be stored outside the repository. Set `SYNDNET_ANALYSIS_DATA_DIR` to that directory when running study analysis commands. The required original derived-input filenames are listed in REPRODUCIBILITY.md. Request access through DATA_ACCESS.md. Generated controlled outputs must not be committed.

# Version 1.1.0

Adds losslessly extracted frozen inference weights, exact component deduplication, safe strict loading, paired-image inference, source provenance, fidelity and clean-environment reports, a model card and Release asset download verification. Preserves every v1.0.0 frozen scientific payload file and numerical output byte-for-byte. The original v1.0.0 tag and Release are unchanged. No alpha, threshold or clinical result is refitted.

# Changelog

## 1.0.0 — publication release preparation

- Preserves the permanently frozen submission code, inputs, configurations, statistical outputs and R environment.
- Adds numerical-reproduction scope, data-access limitations, code availability, citation and archival instructions.
- Adds the standard Apache-2.0 license and separate third-party license records.
- Adds release-integrity tests and reports checks actually performed.

This release preparation changes repository documentation and validation tooling; scientific algorithms, scores, predictions and results are unchanged. Publication status is recorded in `docs/RELEASE_STATUS.json`.

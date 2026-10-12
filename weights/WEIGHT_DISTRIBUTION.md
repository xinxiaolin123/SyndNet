# Checkpoint distribution

Frozen inference checkpoints are distributed as a GitHub Release asset. `scripts/download_weights.py` downloads the published archive and verifies its SHA256 before extraction. Individual state files and tensor contents are identified in `MANIFEST.json` and `SHA256SUMS`.

Checkpoint files are stored separately from the Git source tree. The existing v1.1.0 archive remains the downloadable checkpoint source for this software revision. State tensors, residual scales and the operating threshold are unchanged.

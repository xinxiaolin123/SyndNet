# Frozen inference weights

Version 1.1.0. Tensor-only state dictionaries, loaded with weights_only=True. The MANIFEST records exact hashes, tensor counts, parameter/buffer counts and source checkpoint hashes. Components are deduplicated only after exact tensor equality. Complete reconstructed model states load with strict=True.

Use the matching v1.1.0 code and scripts/infer_pair.py, with the extracted weights directory. CUDA float16 inference is the verified scope. All alpha values, normalization buffers and the global operating threshold are frozen, not refitted. No raw images, clinical records, optimizer or training metadata are included.

Project code and authored model states: Apache-2.0; Copyright 2026 SyndNet authors. Upstream software licences apply separately. No public full-retraining claim. DOI_PENDING.

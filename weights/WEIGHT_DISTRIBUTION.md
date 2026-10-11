# Weight distribution

Ordinary Git contains only inference code, configuration, manifests, hashes, documentation and verification reports. The 30 tensor state dictionaries total 923,867,515 bytes. Ten files exceed 50 MiB and five diagnostic states exceed 100 MiB. Exact sizes and hashes are in `MANIFEST.json`. No tensor checkpoint is committed to normal Git history.

The lossless weight archive is a GitHub v1.1.0 Release asset named `SyndNet_v1.1.0_inference_weights.zip`. Its companion SHA256 file identifies the complete archive. Extract it to obtain a `weights` directory and pass that directory to `scripts/infer_pair.py`. Each tensor file is independently SHA256-verified before safe `weights_only=True` loading; the manifest and inference configuration must match the code release.

Zenodo deposition is not performed by this release step. DOI_PENDING remains until approved publication metadata and an actual DOI-minting deposit exist. A future archival deposit should include the exact v1.1.0 code archive, weight archive and their checksums. GitHub Release assets provide access; they do not by themselves establish DOI-based permanence. Git LFS is not required.

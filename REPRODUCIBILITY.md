# Software reproducibility

Follow [README.md](README.md) for installation, verified checkpoint extraction, inference and public checks. Dependency specifications are in `environments/`. `SHA256SUMS.txt` covers the source distribution; `weights/SHA256SUMS` covers checkpoint states and metadata.

Public checks use artificial examples only. They do not reproduce manuscript statistics. The public reader-study framework describes input formats without actual responses, assignments or study-specific analysis specifications. Clinical inputs remain subject to [controlled access](DATA_ACCESS.md).

Frozen inference requires the supplied model implementation, metadata and runtime context. Full retraining and manuscript analyses require separate study materials and are outside this public software tree. Preserve complete versioned study code privately for editor/reviewer verification; this public tree alone is not a full scientific reproducibility package.

# Inference dependencies

The authoritative final external predictor references 15 seed/fold residual checkpoints. Each contains a complete final PHENOTYPE state: diagnostic baseline, anatomy teacher, reliability calibrator, residual MLPs, risk parameters and anatomical support buffer. The public scientific implementation reconstructs the complete state and loads with `strict=True`.

Tensor equality proves sharing across seeds within each fold. The five folds have distinct diagnostic, teacher and calibrator states; they are not globally shared. The lossless package therefore contains 5 diagnostic states, 5 anatomy states, 5 reliability states and 15 residual states. `weights/checkpoint_dependency_graph.json` records the exact files for every instance. `weights/DEDUPLICATION_REPORT.md` records canonical tensor hashes and exact equality checks.

Diagnostic states include the full trained encoder and prototype mean/scale buffers. Residual states include the locked 8 × 6 anatomical support matrix. No additional private initialization is needed to instantiate inference: constructors use `pretrained=False`, and complete model states supply all tensors. The domain-specific normal SSL checkpoint is an original training initialization dependency, not an additional public inference dependency once the trained diagnostic state is loaded. This distinction does not establish complete retraining reproducibility.

Each reliability state also includes its 12-element feature mean and scale normalization buffers; they are not recomputed. Tensor manifests count parameters and persistent buffers separately.

The remaining required inputs are the 15 frozen alpha scalars, fixed global threshold, exact preprocessing constants, architecture code and aggregation specification. Their public configuration is recorded alongside the tensor manifest. Optimizer, scheduler, scaler, RNG states, patient manifests and training logs are unnecessary for inference and are excluded.

Checkpoint discovery used recursive local inspection and source-script provenance, followed by strict loading, tensor equality and output fidelity. The complete inventory with absolute source paths is private; `weights/checkpoint_discovery_inventory_public.csv` retains nonidentifying file metadata and hashes. Source-component correspondence is recorded without paths in `weights/SOURCE_COMPONENT_EQUIVALENCE.json`.

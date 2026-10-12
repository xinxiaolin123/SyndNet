# Inference dependencies

The original final external predictor references 15 seed/fold residual checkpoints. Each contains a complete final PHENOTYPE state: diagnostic baseline, anatomy teacher, reliability calibrator, residual MLPs, risk parameters and anatomical support buffer. The public scientific implementation reconstructs the complete state and loads with `strict=True`.

Tensor equality establishes sharing across seeds within each fold. The five folds have distinct diagnostic, teacher and calibrator states. The lossless package contains 5 diagnostic states, 5 anatomy states, 5 reliability states and 15 residual states. `weights/checkpoint_dependency_graph.json` identifies the files for every instance, and `weights/MANIFEST.json` records canonical tensor hashes. Loading and component-equivalence evidence is summarized in [inference validation](INFERENCE_VALIDATION.md).

Diagnostic states include the full trained encoder and prototype mean/scale buffers. Residual states include the locked 8 × 6 anatomical support matrix. No additional private initialization is needed to instantiate inference: constructors use `pretrained=False`, and complete model states supply all tensors. The domain-specific normal SSL checkpoint is an original training initialization dependency, not an additional public inference dependency once the trained diagnostic state is loaded. This distinction does not establish complete retraining reproducibility.

Each reliability state also includes its 12-element feature mean and scale normalization buffers; they are not recomputed. Tensor manifests count parameters and persistent buffers separately.

The remaining required inputs are the 15 frozen alpha scalars, fixed global threshold, exact preprocessing constants, architecture code and aggregation specification. Their public configuration is recorded alongside the tensor manifest. Optimizer, scheduler, scaler, RNG states, patient manifests and training logs are unnecessary for inference and are excluded.

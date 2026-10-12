# Final inference specification

For seed s ∈ {42,123,456} and fold f ∈ {0,1,2,3,4}, the original PHENOTYPE module returns diagnostic baseline logit b(s,f,x) and gated anatomy-aligned residual r(s,f,x). The fixed final logit is

`z(s,f,x) = b(s,f,x) + alpha(s,f) * r(s,f,x)`.

For a new examination, `q(s,x) = sigmoid(mean_f z(s,f,x))`, then `P(x) = mean_s q(s,x)`. The binary prediction is `int(P(x) >= 0.012530357984719657)`, with 1 denoting mechanical instability. There is no additional fitted probability calibration or centre-specific threshold. This order is copied from the original external prediction script; averaging all 15 probabilities would be different.

The original pathway runs model forwards with CUDA float16 autocast, then converts baseline logits and residuals to float32 before applying alpha and NumPy aggregation. The supported release preserves this precision policy. CPU inference is not claimed to be fidelity-verified.

The original external predictor uses batch size 4. The single-pair command repeats the same AP/LAT tensors four times, runs that batch, and returns the first result. All model operations act independently on each examination; no batch statistics are fitted. This preserves the size-4 CUDA kernel context without requiring three additional patient examinations. On the locked 40-case external fidelity subset, this single-pair rule matches frozen probabilities within 5.96e-8 with zero decision mismatches. Direct size-1 execution showed a maximum difference of 0.000162661 and 11 values outside 1e-5, with zero decision mismatches; it is not the release command's precision contract. Details are retained in [inference validation](INFERENCE_VALIDATION.md) and `validation/single_pair_context_audit.json`.

Internal frozen inference used batch size 12 and float64 integration in the probe exporter. Replaying it with a different batch context produced a maximum 0.007227 probability difference in the initial sample test. Original size-12 replay passed the unchanged tolerance. Historical internal OOF reproduction therefore requires the original batch context, not just a held-out fold number. This numerical sensitivity is disclosed rather than treating arbitrary batch sizes as interchangeable.

Internal OOF reproduction is a distinct evaluation path: use only the patient's prespecified held-out fold for each seed, average seed probabilities, and apply that fold's inherited threshold. It is used solely to verify frozen OOF predictions. `scripts/infer_pair.py` accepts a new pair without a patient manifest and always uses the 15-instance new-case ensemble and global threshold. It does not select an OOF fold or reproduce a historical internal OOF prediction through the new-case command.

All alpha values are copied from `FINAL_SCALE_WEIGHTS.json`, with its source SHA256 recorded in `weights/integration/alpha_by_checkpoint.json`. The global threshold is copied from `FINAL_FREEZE.json` with provenance in `weights/inference_config.json`; neither alpha nor threshold is refitted.

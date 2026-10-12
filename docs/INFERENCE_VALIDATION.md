# Inference validation

## Checkpoints and loading

Frozen inference comprises five diagnostic states, five anatomy states, five reliability states and fifteen seed/fold residual states. Shared component tensors are identical across seeds within each fold. Each residual state includes its anatomical support buffer. Complete reconstruction of all fifteen models with `strict=True` produced no missing or unexpected keys. Component states were also compared with the original standalone states and were tensor-identical.

Individual state-file and canonical tensor SHA256 values are recorded in `weights/MANIFEST.json`. The published v1.1.0 archive has SHA256 `160aa8f1e976d9aea65bd344dea90b331753aee394e70f453af2f4cae40b02e9`. Checkpoint identity, integration scales and thresholds are unchanged in this documentation revision.

## Environment

Verification used Windows 11, Python 3.12.14, PyTorch 2.14.0+cu132, torchvision 0.29.0+cu132, CUDA 13.2 and an NVIDIA GeForce RTX 5090 D v2. Model forwards use CUDA float16 autocast; logits are converted to float32 before external integration. Internal frozen out-of-fold integration uses float64. Random seed was 0, cuDNN benchmarking was disabled and deterministic cuDNN execution was disabled. Dependency versions are in `environments/inference-verified.txt`.

## Stratified numerical fidelity

The 90-case reference comparison selected five already-approved case codes per fold and label internally and per external centre and label. It included 50 internal out-of-fold cases and 40 external cases. Internal execution used the corresponding held-out fold across three seeds, original size-12 batch context, float64 integration and inherited fold thresholds. External execution used five-fold logit averaging per seed, three-seed probability averaging, original size-4 batches and the locked global threshold.

Mean absolute probability difference was `5.646574278270354e-9`, and maximum difference was `5.960464477539063e-8`. All 90 decisions agreed at their locked thresholds. Machine-readable evidence is in `validation/checkpoint_fidelity_report.json`.

## Batch-context sensitivity

CUDA float16 numerical fidelity depends on inference batch context. In a 50-case internal comparison using a different batch context, the maximum probability difference was approximately `0.0072272264`; there were zero threshold decision changes in that sample. Original size-12 replay restored the numerical fidelity described above.

For 40 external cases, direct size-1 execution differed from the frozen probabilities by at most `0.00016266107559204102`, with 11 differences exceeding `1e-5` and zero decision changes. Four replicated copies of the same pair, with the first output retained, differed by at most `5.960464477539063e-8`, with zero decision changes. This replicated size-4 context is used by `scripts/infer_pair.py`. Details appear in `validation/single_pair_context_audit.json`.

## Full study-cohort comparison

All 2,050 study cases were evaluated locally using controlled images, with the same approved case mapping as the released derived predictions. Only aggregate results are reported. Internal cases use the corresponding held-out fold across the three seeds and inherited fold thresholds. External cases use all five fold logits within each seed, followed by three-seed probability averaging and the locked global threshold. This internal evaluation is distinct from the new-case fifteen-model command.

### Original batch context versus frozen predictions

The original internal size-12 and external size-4 batches were replayed, including the final partial external batch. Internal integration used float64 and external integration float32.

| Cohort | N | Mean | Median | 95th percentile | 99th percentile | Maximum | Discordant decisions | Concordance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| All cases | 2050 | 4.26911216e-19 | 0 | 1.73472348e-18 | 3.46944695e-18 | 1.11022302e-16 | 0 | 100.000000000% |
| Internal OOF | 1461 | 5.99019845e-19 | 0 | 1.73472348e-18 | 3.46944695e-18 | 1.11022302e-16 | 0 | 100.000000000% |
| Centre 1 | 116 | 0 | 0 | 0 | 0 | 0 | 0 | 100.000000000% |
| Centre 2 | 89 | 0 | 0 | 0 | 0 | 0 | 0 | 100.000000000% |
| Centre 3 | 272 | 0 | 0 | 0 | 0 | 0 | 0 | 100.000000000% |
| Centre 4 | 112 | 0 | 0 | 0 | 0 | 0 | 0 | 100.000000000% |

### Four replicated pairs versus frozen predictions

The released single-pair kernel context was applied to each examination. Internal comparisons retain the held-out-fold evaluation and fold threshold; the new-case command itself does not select an internal fold. Differences therefore quantify the sensitivity of frozen evaluation to this alternative execution context.

| Cohort | N | Mean | Median | 95th percentile | 99th percentile | Maximum | Discordant decisions | Concordance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| All cases | 2050 | 2.10476141e-05 | 2.68443027e-07 | 3.11955893e-05 | 0.000351492753 | 0.00722722636 | 0 | 100.000000000% |
| Internal OOF | 1461 | 2.94147312e-05 | 8.36075043e-07 | 4.89492737e-05 | 0.000548502448 | 0.00722722636 | 0 | 100.000000000% |
| Centre 1 | 116 | 5.10086445e-09 | 3.10440858e-10 | 3.97364298e-08 | 5.96046448e-08 | 5.96046448e-08 | 0 | 100.000000000% |
| Centre 2 | 89 | 4.64789263e-09 | 1.55220429e-10 | 3.97364298e-08 | 5.96046448e-08 | 5.96046448e-08 | 0 | 100.000000000% |
| Centre 3 | 272 | 1.89117832e-09 | 1.55220429e-10 | 1.9868215e-08 | 3.97364298e-08 | 3.97364298e-08 | 0 | 100.000000000% |
| Centre 4 | 112 | 1.5282754e-06 | 3.10440858e-10 | 3.97364298e-08 | 5.96046448e-08 | 0.000170469284 | 0 | 100.000000000% |

### Four replicated pairs versus direct size-1 execution

Both contexts use the same state tensors, residual scales, aggregation and operating thresholds. The probability differences below concern computational execution, not a refitted model.

| Cohort | N | Mean | Median | 95th percentile | 99th percentile | Maximum | Discordant decisions | Concordance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| All cases | 2050 | 2.33326191e-05 | 8.69855285e-07 | 5.98223887e-05 | 0.00047152341 | 0.00414466858 | 0 | 100.000000000% |
| Internal OOF | 1461 | 2.79153319e-05 | 7.37141818e-07 | 6.21676445e-05 | 0.00071486237 | 0.00414466858 | 0 | 100.000000000% |
| Centre 1 | 116 | 1.7161221e-05 | 1.73179433e-06 | 0.000103831291 | 0.000222177798 | 0.000444546342 | 0 | 100.000000000% |
| Centre 2 | 89 | 7.15301758e-06 | 7.41332769e-07 | 2.07040466e-05 | 0.000164537429 | 0.00017786026 | 0 | 100.000000000% |
| Centre 3 | 272 | 9.91662364e-06 | 9.82778147e-07 | 2.59794288e-05 | 0.000286480034 | 0.000343233347 | 0 | 100.000000000% |
| Centre 4 | 112 | 1.5383308e-05 | 1.63028017e-06 | 8.96006823e-05 | 0.000166666505 | 0.000298157334 | 0 | 100.000000000% |

No operating-threshold decisions changed in these full-cohort comparisons. The reported probability distributions still delimit the observed batch-context sensitivity.

Machine-readable aggregate results are in `validation/full_cohort_fidelity.json`. Images, private paths and newly computed case-level probabilities are not distributed.

## Clean-environment execution

A separate Python virtual environment installed from the public inference dependency specification executed the paired-image command with nonclinical synthetic grayscale patterns. All fifteen models loaded without missing or unexpected keys. The output probability was `0.6350866556167603`, with threshold `0.012530357984719657` and prediction 1. Runtime was approximately 22.88 seconds on the documented GPU. This test establishes execution and loading only; synthetic patterns provide no evidence of clinical accuracy. The result is recorded in `validation/inference_smoke_test.json`.

## Platform and scientific scope

The verified computational scope is the documented CUDA float16 environment. CPU fidelity and equivalent numerical behaviour on other platforms have not been established. Internal out-of-fold and new-case ensemble predictions are distinct evaluation protocols. Arbitrary batch sizes should not be assumed to reproduce frozen probabilities. No model weights, residual scales, operating thresholds or calibration parameters were refitted for these comparisons.

Across all 2,050 cases, original-context replay agreed with frozen probabilities to a maximum absolute difference of approximately `1.11e-16`. Replicated size-4 versus frozen execution differed by as much as `0.0072272264`, and replicated size-4 versus direct size-1 by as much as `0.0041446686`. All locked threshold decisions agreed in all three comparisons. These probability differences are larger than the `1e-5` tolerance used in the earlier stratified validation and should not be characterized as uniformly negligible rounding differences.

The largest external replicated-pair difference, approximately `0.0001704693` in Centre 4, concerns the original final partial batch, which contained one examination. Four replicated copies change that original size-1 execution context. Replicated-pair execution therefore does not uniformly reproduce every frozen partial-batch probability within `1e-5`, despite complete threshold-decision concordance in this study. Original-context replay is required for numerical reproduction of those records.

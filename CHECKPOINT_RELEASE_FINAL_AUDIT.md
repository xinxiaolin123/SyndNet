# Checkpoint release final audit

Final status: **PASS** for the documented CUDA inference release. No remote publication is permitted before the retained reports and schema check pass.

1. **Required families:** 5 diagnostic, 5 anatomy, 5 reliability, 15 residual; 15 alpha values; prototype, calibrator normalization and support buffers included.

2. **Exact public files:** Tracked-file inventory in checkpoint_release_final_audit.json; weight files in MANIFEST.json.

3. **Exact excluded files:** 484 original checkpoints listed by SHA256 in weights/EXCLUDED_CHECKPOINTS.csv; private absolute-path inventory, all raw images, patient manifests and training states excluded.

4. **All weight SHA256:** PASS: MANIFEST.json and weights/SHA256SUMS; complete archive 160aa8f1e976d9aea65bd344dea90b331753aee394e70f453af2f4cae40b02e9.

5. **Strict loading:** PASS: 15 complete model states; zero missing/unexpected keys; weights_only=True.

6. **End-to-end inference:** PASS: fresh environment, public adapter, synthetic paired image, all 15 instances.

7. **Frozen fidelity:** PASS: 90 cases, maximum absolute difference 5.96e-8, zero decision mismatches; not a full 2050-case rerun.

8. **Threshold concordance:** PASS against frozen derived data and provenance; internal OOF inherited thresholds remain distinct from the new-case global threshold; manuscript text itself was not supplied.

9. **Clean environment:** PASS: newly created venv from public dependencies, isolated Python -I, no private scientific modules.

10. **Privacy scan:** PASS: retained approved derived case/reader codes only; tensor-only weight payload; no images or source clinical records.

11. **Credential scan:** PASS: all publication candidates scanned; no matched secrets.

12. **Absolute-path scan:** PASS: no private absolute paths in publication candidates.

13. **Large-file strategy:** PASS: 923867515 tensor bytes; 10 files >50 MiB, 5 >100 MiB; all hosted as Release asset, none in Git.

14. **README consistency:** PASS: inference upgraded after fidelity/smoke PASS; numerical results and full-retraining limits distinguished.

15. **REPRODUCIBILITY consistency:** PASS: manifest, archive, environment, command and numerical context limitations recorded.

16. **DATA_ACCESS consistency:** PASS: public weights and controlled imaging/records/annotations/manifests distinguished.

17. **CODE_AVAILABILITY consistency:** PASS: verified CUDA inference scope, no full public retraining claim.

18. **CITATION consistency:** PASS (CFF 1.2.0 schema validated): version 1.1.0; no invented DOI or individual authors.

19. **GitHub readiness:** PASS: publish only this new tag/Release; v1.0.0 remains unchanged.

20. **Zenodo readiness:** Technical code/weight archives prepared; manual author metadata review pending; no deposit or DOI created.

## Weight identity

| File | SHA256 | Bytes | Strict load |
|---|---|---:|---|
| `diagnostic/fold_0_b73bede5dc80.pt` | `0b587df298cbe8bc0d572af339745432b96a7075710d61177ac498503fe0cc16` | 125839087 | PASS |
| `anatomy/fold_0_802ef43dc0bd.pt` | `76cb7e066b71a2b9377f296d9708c07848190e9d7bd497f17294425dd378635b` | 57585561 | PASS |
| `reliability/fold_0_60357e219af4.pt` | `fd58b7d3751f9c2363715ddc95a3be244fedd5f6069e3ce2af02655f8632a411` | 4117 | PASS |
| `residual/seed_42/fold_0.pt` | `c6fdecee07013bfda4fbff101e4d2c185c6c803c98be9fa2a97e2c2f9552c712` | 448246 | PASS |
| `diagnostic/fold_1_3d92b02b7aea.pt` | `28a0dc690bba2d0bcccbc30d98ff54c4894c0a62e1d0b8ded2a7a85b43fe2b41` | 125839087 | PASS |
| `anatomy/fold_1_933db1691190.pt` | `e063f0898f4d6a7d9dc44d79a233660d429c83f29eb3e2e07c65f11196fac475` | 57585561 | PASS |
| `reliability/fold_1_80da98941130.pt` | `0f9c40c4428828fc21ff5ff9a0b2fda40893a3ceddae3def5ea187d9ac937c1f` | 4117 | PASS |
| `residual/seed_42/fold_1.pt` | `e72c8f7aa6c338762bcd6be49dc949977aaa3a52b23ae9a48b8848fb16300819` | 448246 | PASS |
| `diagnostic/fold_2_baecb3687e79.pt` | `82c1de08b4b9a041379d2b0c4e2cd0fbd1db40af3bf1e3084b3f46f03dc48b99` | 125839087 | PASS |
| `anatomy/fold_2_6fb458d1aeef.pt` | `4bf0b387b66e7bc28bc1875c20928cad5a4c3ca5d39db990a669fccfb5e88b61` | 57585561 | PASS |
| `reliability/fold_2_5b5a8c9fe403.pt` | `eb1287178f98f88e6f7f42426e33c799ebe396fa6c49d5c1bfeaff71a585add6` | 4117 | PASS |
| `residual/seed_42/fold_2.pt` | `ed0e7b5ebfc03bcb4f49b514bb831e5954b0d9b19e6f4c5eb8b1d2b64eaa5d5e` | 448246 | PASS |
| `diagnostic/fold_3_8b007083577a.pt` | `0e13132e9561d82348aae358809676ebe8755252dd7a224cc02cf22dfbdcfcff` | 125839087 | PASS |
| `anatomy/fold_3_fa03668b6898.pt` | `377efb10e28df214ea96850e40372f7fcab73f68b2e0c78209d45fd4afbecb91` | 57585561 | PASS |
| `reliability/fold_3_d3bb7426a356.pt` | `7730413b07e99edce122204e4139b600d03995a256861e03e86e09fbf2ea2b17` | 4117 | PASS |
| `residual/seed_42/fold_3.pt` | `22f34ff46d26efad825fd9924dd1997a793659f2da633a65ac01caeae176e82a` | 448246 | PASS |
| `diagnostic/fold_4_4577de2a8733.pt` | `20da3f3197abd37638bfe8cadbc6c474811cd14e8e776f49d2397213fefc460e` | 125839087 | PASS |
| `anatomy/fold_4_d4f1c8285969.pt` | `31c610383cab5e2f394ccf999d0cffb14279df463aeda99faabb5742d6519483` | 57585561 | PASS |
| `reliability/fold_4_f1475aa90d59.pt` | `d2b8d4b3cc0c4989f3dbed854e1617b69299b033c9d4523574c6697acc168a18` | 4117 | PASS |
| `residual/seed_42/fold_4.pt` | `dae8469f6a2b6601a2f63b1eaf2262930885047d83543da04d03ebf78a1c24f1` | 448246 | PASS |
| `residual/seed_123/fold_0.pt` | `2acd30930773e9aafc191c47b129b47be01765422dda068647fd749726596954` | 448246 | PASS |
| `residual/seed_123/fold_1.pt` | `a5e742746ff7c5d3a0c8ad6843fbc868988ce96fb34bacdaaa1ab5682c4f43e2` | 448246 | PASS |
| `residual/seed_123/fold_2.pt` | `852c785842e7c416c525cd98616e2befa296881cc084fc89233a90ab06f642f6` | 448246 | PASS |
| `residual/seed_123/fold_3.pt` | `d00fe94f7a012018ceb37e13debb463d9fd1d2a7d8e7d1ff490da9244affed32` | 448246 | PASS |
| `residual/seed_123/fold_4.pt` | `4f710e12cba50d08715630c48cf4b65c2fb2089a8e1e1e37fc802c87952e3ebc` | 448246 | PASS |
| `residual/seed_456/fold_0.pt` | `d9fd85ceb43bad1d9ada97c38d2e91e15e3bf318fc5de19b3a6c82544f11e0ac` | 448246 | PASS |
| `residual/seed_456/fold_1.pt` | `9eb7912bdf0e36576d019c0c609fc923542a19075cef1da88d69d365da525027` | 448246 | PASS |
| `residual/seed_456/fold_2.pt` | `d4037bbf906985e29838c6cd3b34835d668732fe107742ff3c056fb500fab685` | 448246 | PASS |
| `residual/seed_456/fold_3.pt` | `02e82c9ce2ab4fc5f7cf7ab3548ae7c222182437d264cb9e4ff1d7d8ddcbcf5d` | 448246 | PASS |
| `residual/seed_456/fold_4.pt` | `def8f5e6046b403b67e2e429b6b77ae74b33dc477a86066f8d91211b46f03aab` | 448246 | PASS |

## Practical limits

- Pattern screening is not proof of institutional publication permission.
- CUDA float16 batch-size context is locked; alternate batch sizes showed numerical sensitivity and are documented.
- Cross-platform/hardware numerical fidelity and CPU inference are not established.
- Raw imaging and retraining inputs remain controlled; no full public retraining or clinical deployment claim.

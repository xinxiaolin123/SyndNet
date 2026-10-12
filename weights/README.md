# Final frozen inference checkpoints

The current source tree contains only metadata for final inference states; tensors are distributed separately. No intermediate checkpoint, optimizer state or training snapshot is included. State files are unchanged from the validated model.

Use `python scripts/download_weights.py --output-dir downloaded_weights`, then `python scripts/infer_pair.py --ap path/to/AP.png --lat path/to/LAT.png --weights-dir downloaded_weights/weights --output prediction.json`. The downloader verifies the existing published archive. Each file SHA256 below is verified before loading; canonical tensor hashes are recorded in `MANIFEST.json`.

| Checkpoint name | Purpose | SHA256 |
|---|---|---|
| `diagnostic/fold_0_b73bede5dc80.pt` | Trained diagnostic encoder and prototype buffers | `0b587df298cbe8bc0d572af339745432b96a7075710d61177ac498503fe0cc16` |
| `anatomy/fold_0_802ef43dc0bd.pt` | Probabilistic anatomical-anchor teacher | `76cb7e066b71a2b9377f296d9708c07848190e9d7bd497f17294425dd378635b` |
| `reliability/fold_0_60357e219af4.pt` | Anchor reliability calibration and normalization | `fd58b7d3751f9c2363715ddc95a3be244fedd5f6069e3ce2af02655f8632a411` |
| `residual/seed_42/fold_0.pt` | Seed/fold anatomy-aligned residual and support buffer | `c6fdecee07013bfda4fbff101e4d2c185c6c803c98be9fa2a97e2c2f9552c712` |
| `diagnostic/fold_1_3d92b02b7aea.pt` | Trained diagnostic encoder and prototype buffers | `28a0dc690bba2d0bcccbc30d98ff54c4894c0a62e1d0b8ded2a7a85b43fe2b41` |
| `anatomy/fold_1_933db1691190.pt` | Probabilistic anatomical-anchor teacher | `e063f0898f4d6a7d9dc44d79a233660d429c83f29eb3e2e07c65f11196fac475` |
| `reliability/fold_1_80da98941130.pt` | Anchor reliability calibration and normalization | `0f9c40c4428828fc21ff5ff9a0b2fda40893a3ceddae3def5ea187d9ac937c1f` |
| `residual/seed_42/fold_1.pt` | Seed/fold anatomy-aligned residual and support buffer | `e72c8f7aa6c338762bcd6be49dc949977aaa3a52b23ae9a48b8848fb16300819` |
| `diagnostic/fold_2_baecb3687e79.pt` | Trained diagnostic encoder and prototype buffers | `82c1de08b4b9a041379d2b0c4e2cd0fbd1db40af3bf1e3084b3f46f03dc48b99` |
| `anatomy/fold_2_6fb458d1aeef.pt` | Probabilistic anatomical-anchor teacher | `4bf0b387b66e7bc28bc1875c20928cad5a4c3ca5d39db990a669fccfb5e88b61` |
| `reliability/fold_2_5b5a8c9fe403.pt` | Anchor reliability calibration and normalization | `eb1287178f98f88e6f7f42426e33c799ebe396fa6c49d5c1bfeaff71a585add6` |
| `residual/seed_42/fold_2.pt` | Seed/fold anatomy-aligned residual and support buffer | `ed0e7b5ebfc03bcb4f49b514bb831e5954b0d9b19e6f4c5eb8b1d2b64eaa5d5e` |
| `diagnostic/fold_3_8b007083577a.pt` | Trained diagnostic encoder and prototype buffers | `0e13132e9561d82348aae358809676ebe8755252dd7a224cc02cf22dfbdcfcff` |
| `anatomy/fold_3_fa03668b6898.pt` | Probabilistic anatomical-anchor teacher | `377efb10e28df214ea96850e40372f7fcab73f68b2e0c78209d45fd4afbecb91` |
| `reliability/fold_3_d3bb7426a356.pt` | Anchor reliability calibration and normalization | `7730413b07e99edce122204e4139b600d03995a256861e03e86e09fbf2ea2b17` |
| `residual/seed_42/fold_3.pt` | Seed/fold anatomy-aligned residual and support buffer | `22f34ff46d26efad825fd9924dd1997a793659f2da633a65ac01caeae176e82a` |
| `diagnostic/fold_4_4577de2a8733.pt` | Trained diagnostic encoder and prototype buffers | `20da3f3197abd37638bfe8cadbc6c474811cd14e8e776f49d2397213fefc460e` |
| `anatomy/fold_4_d4f1c8285969.pt` | Probabilistic anatomical-anchor teacher | `31c610383cab5e2f394ccf999d0cffb14279df463aeda99faabb5742d6519483` |
| `reliability/fold_4_f1475aa90d59.pt` | Anchor reliability calibration and normalization | `d2b8d4b3cc0c4989f3dbed854e1617b69299b033c9d4523574c6697acc168a18` |
| `residual/seed_42/fold_4.pt` | Seed/fold anatomy-aligned residual and support buffer | `dae8469f6a2b6601a2f63b1eaf2262930885047d83543da04d03ebf78a1c24f1` |
| `residual/seed_123/fold_0.pt` | Seed/fold anatomy-aligned residual and support buffer | `2acd30930773e9aafc191c47b129b47be01765422dda068647fd749726596954` |
| `residual/seed_123/fold_1.pt` | Seed/fold anatomy-aligned residual and support buffer | `a5e742746ff7c5d3a0c8ad6843fbc868988ce96fb34bacdaaa1ab5682c4f43e2` |
| `residual/seed_123/fold_2.pt` | Seed/fold anatomy-aligned residual and support buffer | `852c785842e7c416c525cd98616e2befa296881cc084fc89233a90ab06f642f6` |
| `residual/seed_123/fold_3.pt` | Seed/fold anatomy-aligned residual and support buffer | `d00fe94f7a012018ceb37e13debb463d9fd1d2a7d8e7d1ff490da9244affed32` |
| `residual/seed_123/fold_4.pt` | Seed/fold anatomy-aligned residual and support buffer | `4f710e12cba50d08715630c48cf4b65c2fb2089a8e1e1e37fc802c87952e3ebc` |
| `residual/seed_456/fold_0.pt` | Seed/fold anatomy-aligned residual and support buffer | `d9fd85ceb43bad1d9ada97c38d2e91e15e3bf318fc5de19b3a6c82544f11e0ac` |
| `residual/seed_456/fold_1.pt` | Seed/fold anatomy-aligned residual and support buffer | `9eb7912bdf0e36576d019c0c609fc923542a19075cef1da88d69d365da525027` |
| `residual/seed_456/fold_2.pt` | Seed/fold anatomy-aligned residual and support buffer | `d4037bbf906985e29838c6cd3b34835d668732fe107742ff3c056fb500fab685` |
| `residual/seed_456/fold_3.pt` | Seed/fold anatomy-aligned residual and support buffer | `02e82c9ce2ab4fc5f7cf7ab3548ae7c222182437d264cb9e4ff1d7d8ddcbcf5d` |
| `residual/seed_456/fold_4.pt` | Seed/fold anatomy-aligned residual and support buffer | `def8f5e6046b403b67e2e429b6b77ae74b33dc477a86066f8d91211b46f03aab` |

Five diagnostic, five anatomy and five reliability states are shared across seeds within each fold. Fifteen residual states complete the three-seed/five-fold graph. Fixed integration parameters and the operating threshold are in `inference_config.json` and `integration/`.

Expected usage is paired preoperative AP/lateral inference within the documented study and computational scope. See `../docs/INFERENCE_VALIDATION.md` for strict loading, original-context fidelity and batch-context sensitivity. Authored states use Apache-2.0; Copyright 2026 SyndNet authors. Dependency licences apply separately.

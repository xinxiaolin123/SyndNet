# Public repository audit

Repository: [SyndNet](https://github.com/xinxiaolin123/SyndNet). Audit date: 12 October 2026. Audited baseline commit: `015278bf8f51641b8b4f2c8f3f5a635a6733b45b`. All 398 baseline file contents were verified against their Git blob hashes before review.

## Scope and outcome

The current publication tree contains scientific source, aggregate reference tables, final checkpoint metadata, environment documentation and explicitly synthetic formats. Case-level study inputs, actual reader records, reader assignments and reader-level exports were removed from the current tree. Statistical formulas, model tensors, residual scales, operating thresholds and retained aggregate estimates were not changed. Full numerical and reader-study reproduction requires approved controlled inputs outside the repository.

This audit covers the current source tree. Removing files from the current branch does **not** erase earlier Git objects, tags or downloaded copies. Historical v1.0.0/v1.1.0 trees and code Release assets retain the earlier derived study and reader inputs. They require a separately approved history/archive treatment; this repository must not be described as cleared across its entire history. No existing tag or Release was rewritten, and no new GitHub Release was created.

## Files removed or restricted

Removed case-level input files:

- `data/ablation_patient_predictions.csv`
- `data/final_model_predictions.csv`
- `data/individual_reader_scores.csv`
- `data/reader_study_model_predictions.csv`
- `data/supplementary_discrimination_predictions.csv`
- `MRMC/01_input/MRMC_REAL_READER_CASE_FINAL.csv`
- `MRMC/01_input/MRMC_REAL_LONG_FINAL.csv`
- `MRMC/01_input/MRMC_LOCKED_CASE_PREDICTIONS.csv`

Removed reader-level and confidential output groups include the original `MRMC/03_results/reader*.csv`, `primary_imrmc_perReader.csv`, `publication_tableS9.csv`, reader ROC exports, original model ROC thresholds, fitted-output summaries and reader metadata. Actual assignments were also removed from the statistical documentation and from the hardcoded R lookup. The assignment lookup now reads the approved controlled input table.

The original `MRMC/04_QC/` files are not distributed in the new reader directory. Their required aggregate reference fingerprint must be supplied with the controlled input bundle. Original individual-reader rows were removed from `results/supplementary_ci.csv` and `results/reproduced_supplementary_ci.csv`; retained aggregate rows preserve their values. Case-level `docs/checkpoint_fidelity_results.csv` and `docs/single_pair_fidelity_results.csv` were removed; aggregate JSON verification records remain.

Development audit files, training histories, experiment/discovery inventories and redundant construction metadata were removed. Unnecessary harvested dependency licence copies were removed because dependency software is not bundled; `LICENSE`, `NOTICE` and `THIRD_PARTY_NOTICES.md` remain. Removed baseline path counts by group: {'root': 5, 'MRMC': 57, 'data': 5, 'docs': 12, 'environments': 1, 'results': 2, 'third_party': 229, 'weights': 4}. Statistical aggregate tables moved to `results/reader_study/` are relocations, not discarded numerical evidence.

## Files and directories renamed

- `MRMC/` → `reader_study_reproducibility/`.
- `02_R/` → `R/`; `05_environment/` → `environment/` within that directory.
- `MRMC_METHODS_FINAL_FACTS.md` → `STATISTICAL_METHODS.md`.
- `MRMC_RESULTS_FINAL_FACTS.md` → `REFERENCE_RESULTS.md`.
- Selected group-level result CSVs moved from the original reader results directory to `results/reader_study/`; no individual-reader tables were retained there.
- `data/` now contains `README.md`, `example_manifest.csv` and `synthetic_examples/` only.

The reader directory contains analysis scripts, methods, software-environment documentation and artificial format examples. Actual study inputs and generated private outputs are external. The R runner refuses an absent or in-repository controlled workspace. Python study analyses similarly require external controlled data; individual-reader supplementary exports require an external output directory.

## Privacy checks performed

The prepared tree was checked recursively for identifiers, accession/patient fields, real study case codes, reader codes, assignments, unintended email addresses, machine-specific Windows/Linux paths, credential patterns, binary imaging files and clinical spreadsheet formats. CSV headers and rows were reviewed to distinguish aggregate references from case- or reader-level records. Public examples use explicit artificial labels and values and are not study records.

No actual patient names, accession numbers, hospital names, raw radiographs, DICOM files, clinical Excel workbooks or confidential record tables are retained in the current tree. The removed study records used de-identified case/reader codes, but were withdrawn under the current controlled-data policy. Hospital-specific source identifiers are not public; aggregate centre labels are retained as study strata. The intended contact is **2060753088@qq.com**. Xinxiao Lin, the confirmed ORCID and the repository's GitHub account URL are intentional publication metadata.

Source configurations use relative paths and runtime-provided external directories. Scanner pattern definitions are detection code, not machine paths. `scripts/check_public_privacy.py` verifies that the full tracked tree is covered by its SHA256 manifest, disallows clinical/binary record files, checks email/path/identifier patterns and confines grouping-field examples to explicitly artificial formats. These checks support source review; they do not assert erasure of historical data or prove anonymization independently.

## Reproducibility checks

- Five Python numerical exports recomputed using controlled external inputs and agreed exactly after full-precision parsing with the original reference results.
- The complete R 4.6.1 reader-study pipeline was rerun using external controlled inputs, including the approved assignment lookup. All **27** original result CSVs agreed exactly in numerical values.
- Retained aggregate result files preserve their original bytes; supplementary tables retain their original aggregate values while removing individual-reader rows.
- Python syntax, analysis imports, unit tests, source/weight SHA256 integrity, checkpoint manifest relationships, artificial formats and privacy checks were verified. Lightweight GitHub Actions runs these public-only checks without clinical inputs or the large checkpoint download.
- The downloader extracted only **30 final tensor files** from the existing verified archive and supplied current metadata. All **15** model instances loaded strictly without missing/unexpected keys in the isolated CUDA environment. The nonclinical example probability remained `0.6350866556167603` with the fixed threshold `0.012530357984719657`. This is execution verification, not new evidence of diagnostic accuracy.
- Prior aggregate full-cohort fidelity and batch-context limitations remain in [inference validation](INFERENCE_VALIDATION.md). Privacy cleanup did not change inference mathematics or re-estimate results.

The new public data scope changes access, not statistics: synthetic examples cannot reproduce publication estimates. Reproduction requires the controlled-data request process in [DATA_ACCESS.md](../DATA_ACCESS.md).

## Final checkpoints and metadata

Only final frozen inference states are referenced. Intermediate checkpoints, optimizer states, training snapshots and failed-experiment inventories are absent from the current source tree. [Weights documentation](../weights/README.md) lists every final file, purpose, SHA256 and expected use. The checkpoint tensors and their canonical hashes are unchanged.

`CITATION.cff` identifies **Xinxiao Lin**, ORCID **0009-0006-6476-2559**, version 1.1.1 and Apache-2.0. No article DOI has been added. Software DOI and the actual release date will be recorded when archival and release are authorized. The Apache-2.0 LICENSE remains the standard unmodified text.

## Remaining manual actions

1. Review and explicitly authorize how to handle confidential derived records in earlier commits, immutable tags, code Release archives and existing copies. A current-branch cleanup does not resolve that historical exposure.
2. Review this revision and approve any future GitHub Release. No new Release or tag is created by this audit.
3. Complete Zenodo archival and add the real software DOI afterward; do not fabricate an article DOI or archive identifier.
4. Keep granted controlled inputs and generated reader-level outputs outside the public repository. Apply the confirmed institutional/data-custodian review and data-use conditions.

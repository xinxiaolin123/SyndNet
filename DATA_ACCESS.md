# Data access

## Released derived materials

`data/` contains release-specific de-identified case codes, reference labels, model probabilities, fixed predictions, model/seed/fold/cohort information, and individual-reader scores. `MRMC/01_input/` contains clean paired reader records, condition-level records, and recorded model predictions. Reader codes R01–R15 are pseudonyms; they are not reader names. Numeric publication exports are in `results/` and `MRMC/03_results/`.

These files are the approved derived materials in the frozen submission archive. They do not contain raw radiographs, DICOM images, original clinical spreadsheets, identifiable source workbooks, or identifiable source clinical records. Public pseudonymization does not independently guarantee that all linkage risks are eliminated.

## Materials not released

Raw radiographic data, restricted landmark/ROI annotations, clinical source records, and restricted study manifests are not supplied. Training-only initialization checkpoints are not distributed; they are not additional inference dependencies because complete trained diagnostic states are included. Access eligibility, institutional approval, consent conditions, and a contact/access mechanism are not documented in the supplied archive; no access promise, email address, or ethics identifier is invented. Authors must specify any lawful controlled-access route in the manuscript's Data Availability statement.

The Apache-2.0 software license does not establish consent, ownership, or access rights for unavailable clinical materials. Third-party and controlled-access materials are not relicensed by this repository.

## Public inference weights

Frozen inference states, normalization buffers, anatomical support, per-instance alpha values and locked configuration are public v1.1.0 Release materials. They contain tensors and nonidentifying configuration only. See `weights/MANIFEST.json` and `weights/WEIGHT_DISTRIBUTION.md`. This addition does not make controlled clinical materials public or establish full retraining reproducibility.

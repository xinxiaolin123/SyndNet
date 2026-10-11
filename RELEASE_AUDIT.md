# Public-release safety audit

Status: PASS. The frozen submission archive was inspected before repository construction. No scientific material was deleted or regenerated. Private review staging is ignored by Git and is not part of the public repository.

Input SHA256: `da559b37913fd0ce829557d4e5fac9abfe218405f89748de7b665f6a8edc9eb7`. Files recursively inspected: 106. Findings: 0.

## Safety scope

- patient names: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- MRNs / hospital numbers: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- accession numbers: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- dates of birth: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- potentially identifying examination dates: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- phone numbers: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- addresses: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- DICOM UIDs: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- institution-internal IDs: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- reader identities: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- absolute Windows paths: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- absolute Linux/server paths: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- usernames: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- passwords / API tokens / SSH keys / cloud credentials / GitHub tokens: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- internal IP addresses / private hostnames: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- signed ethics documents: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- raw clinical records: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- raw radiographs / DICOM: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- unapproved original clinical spreadsheets: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- excluded imaging checkpoints: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.
- temporary logs: filename, text/schema, archive-member and available binary-string screening performed; flagged items remain quarantined.

## Scientific authority

The final submission archive is the release authority. Scientific implementation, configurations, derived inputs and frozen result files are preserved byte-for-byte. Manuscript-specific claims still require comparison with the manuscript text, which is not supplied here.

## Licensing and reproducibility scope

Project code uses the standard Apache License 2.0. Copyright 2026 SyndNet authors. Third-party dependencies retain their upstream licenses separately. DOI_PENDING denotes archival status, not a minted DOI. Frozen imaging checkpoints and raw images are absent; inference on new images and complete retraining are not claimed. Pseudonymous case codes and R01-R15 reader codes occur in the approved derived data. Pattern screening cannot independently prove the absence of all re-identification risk.

## Findings


Policy references: [Nature Communications policy guide](https://www.nature.com/ncomms/submit/policy), [Nature code-publication guidance](https://media.nature.com/full/nature-cms/documents/GuidelinesCodePublication.pdf). GitHub is a version-control access point; a frozen version still requires a DOI-minting archive for permanent citation.

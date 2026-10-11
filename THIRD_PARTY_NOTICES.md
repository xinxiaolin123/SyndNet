# Third-party software notices

Copyright 2026 SyndNet authors applies to SyndNet original code. Its Apache-2.0 license does not replace the licenses of third-party dependencies. No dependency binaries or upstream package source distributions are bundled in the frozen submission archive.

Available upstream notices from the actual installed numerical Python distributions are preserved under `third_party/python/`. The supplied minimum-version license texts for PyTorch and torchvision are preserved separately with their official sources; neither imaging dependency was installed or tested here. Those texts do not assert that every future version has identical licensing terms.

The actual clean R environment's package DESCRIPTION license declarations are recorded verbatim in `third_party/R_PACKAGE_LICENSES.csv`. Available LICENSE/COPYING/NOTICE files are preserved by package under `third_party/R/`. Where a declaration references a standard license without a supplied package-local text, the record retains that declaration rather than inventing a replacement license. R's available COPYING files are also retained.

`third_party/license_provenance.json` records sources, versions and copied files. License metadata may cover bundled upstream components inside dependency wheels; preserve those notices when redistributing those dependencies. These notices are separate from, and do not add academic-only, non-commercial, or clinical-use restrictions to, the unmodified SyndNet Apache-2.0 LICENSE.

## Inference verification environment

Actual installed PyTorch 2.14.0+cu132, torchvision 0.29.0+cu132 and associated package licence texts are retained separately under `third_party/inference_environment/`, with relative source mappings in `provenance.json`. Historical minimum-version notices remain for the preserved original requirements. No dependency binary is bundled in the model archive.

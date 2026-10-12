# Third-party notices

SyndNet project code is distributed under the Apache License 2.0. The repository specifies dependencies without bundling third-party source code, compiled libraries or installation distributions. Installed dependencies retain their respective upstream licences and notices.

Python dependencies include PyTorch, torchvision, timm, NumPy, SciPy, pandas, scikit-learn and Pillow. R analyses use iMRMC, lme4, statmod and their dependencies. Exact dependency versions are recorded in `environments/` and `reader_study_reproducibility/environment/`. Users distributing installed environments should retain the licence files supplied with those distributions.

The model states are authored SyndNet tensors. Complete trained diagnostic states include encoder and prototype buffers; an additional training initialization checkpoint is not required for inference. The repository does not distribute pretrained dependency packages or third-party training initialization assets.

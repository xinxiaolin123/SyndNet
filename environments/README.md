# Environments

The original `requirements.txt` and `environment.yml` in the root are unchanged. They are dependency specifications with version ranges; no historical exact Python environment was supplied. `analysis-verified.txt` records the actual separately tested numerical Python environment, without installing imaging/training dependencies.

The actual clean R environment is `MRMC/05_environment/renv.lock`, `sessionInfo.txt`, and `package_versions.csv`. These are preserved exactly; no second conflicting R lock is introduced. Restore from the `MRMC` directory as described in REPRODUCIBILITY.md.

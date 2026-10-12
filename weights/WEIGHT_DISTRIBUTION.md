# Checkpoint distribution

Use `python scripts/download_weights.py --output-dir downloaded_weights`. The existing archive is verified before final tensor files are extracted. Current repository metadata are copied alongside the states. An existing local archive can be supplied with `--archive`.

See [README.md](README.md) for file names, purposes, SHA256 checksums and expected usage. Only final tensor states are used; optimizer states and training snapshots are not loaded.

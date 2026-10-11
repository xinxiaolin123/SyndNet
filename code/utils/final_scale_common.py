from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from pathlib import Path

import numpy as np
from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score


ROOT = Path(os.environ.get("SYNDNET_WORK_DIR", "work"))
OUTPUTS = ROOT / "outputs"
AUTHORITIES = OUTPUTS / "authorities"
PROBES = OUTPUTS / "probes"
FINAL = OUTPUTS / "final"


def load_config() -> dict:
    return json.loads(Path(os.environ.get("SYNDNET_CONFIG", str(Path(__file__).resolve().parent.parent.parent / "configs" / "final_scale_config.json"))).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows and not fieldnames:
        raise ValueError(f"fieldnames required for empty CSV: {path}")
    names = fieldnames or list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=names, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def logit(p: np.ndarray | float) -> np.ndarray:
    p = np.asarray(p, dtype=float)
    p = np.clip(p, 1e-7, 1 - 1e-7)
    return np.log(p / (1 - p))


def sigmoid(x: np.ndarray | float) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    return np.where(x >= 0, 1 / (1 + np.exp(-x)), np.exp(x) / (1 + np.exp(x)))


def threshold_for_sensitivity(y: np.ndarray, p: np.ndarray, target: float = 0.95) -> float:
    positives = np.sort(np.asarray(p)[np.asarray(y) == 1])
    if positives.size == 0:
        raise ValueError("threshold training set has no positive patients")
    allowed_fn = int(math.floor((1.0 - target) * positives.size + 1e-12))
    index = min(max(allowed_fn, 0), positives.size - 1)
    return float(positives[index])


def metrics(y: np.ndarray, p: np.ndarray, thresholds: np.ndarray | None = None) -> dict[str, float | int]:
    y = np.asarray(y, dtype=int)
    p = np.clip(np.asarray(p, dtype=float), 1e-7, 1 - 1e-7)
    out: dict[str, float | int] = {
        "n": int(y.size),
        "positives": int(y.sum()),
        "auroc": float(roc_auc_score(y, p)),
        "ap": float(average_precision_score(y, p)),
        "brier": float(brier_score_loss(y, p)),
        "log_loss": float(log_loss(y, p, labels=[0, 1])),
    }
    if thresholds is not None:
        pred = p >= np.asarray(thresholds, dtype=float)
        tp = int(((pred == 1) & (y == 1)).sum())
        tn = int(((pred == 0) & (y == 0)).sum())
        fp = int(((pred == 1) & (y == 0)).sum())
        fn = int(((pred == 0) & (y == 1)).sum())
        out.update({
            "sensitivity": tp / max(1, tp + fn),
            "specificity": tn / max(1, tn + fp),
            "tp": tp, "tn": tn, "fp": fp, "fn": fn,
        })
    return out


def stratified_bootstrap_deltas(y: np.ndarray, anchor: np.ndarray, candidate: np.ndarray,
                                iterations: int, seed: int = 20260920) -> dict:
    y = np.asarray(y, dtype=int)
    anchor = np.asarray(anchor, dtype=float)
    candidate = np.asarray(candidate, dtype=float)
    rng = np.random.default_rng(seed)
    groups = [np.flatnonzero(y == value) for value in (0, 1)]
    names = ("auroc", "ap", "brier", "log_loss")
    draws = {name: np.empty(iterations, dtype=np.float64) for name in names}
    for i in range(iterations):
        idx = np.concatenate([rng.choice(group, group.size, replace=True) for group in groups])
        ma = metrics(y[idx], anchor[idx])
        mc = metrics(y[idx], candidate[idx])
        for name in names:
            draws[name][i] = float(mc[name]) - float(ma[name])
    observed_a = metrics(y, anchor)
    observed_c = metrics(y, candidate)
    return {
        name: {
            "candidate_minus_phenotype": float(observed_c[name]) - float(observed_a[name]),
            "ci95": [float(np.quantile(draws[name], 0.025)), float(np.quantile(draws[name], 0.975))],
        }
        for name in names
    }

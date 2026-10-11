"""Deployment wrapper for the internally selection_met PHENOTYPE residual-scale candidate.

The wrapped PHENOTYPE model remains unchanged.  Each seed/fold checkpoint has one
training-only scalar alpha.  Disabling the wrapper returns the original PHENOTYPE
logit bit-for-bit.
"""
from __future__ import annotations

import json
from pathlib import Path

import torch
from torch import nn


class FINAL_SCALEResidualScale(nn.Module):
    def __init__(self, matched_residual_model: nn.Module, alpha: float, enabled: bool = True):
        super().__init__()
        self.phenotype = matched_residual_model
        self.alpha = float(alpha)
        self.enabled = bool(enabled)
        for parameter in self.phenotype.parameters():
            parameter.requires_grad_(False)

    def forward(self, ap: torch.Tensor, lat: torch.Tensor):
        output = self.phenotype(ap, lat)
        if not self.enabled:
            final_logit = output["logit"]
        else:
            final_logit = output["baseline_logit"] + self.alpha * output["biomechanical_residual"]
        result = dict(output)
        result["phenotype_logit"] = output["logit"]
        result["logit"] = final_logit
        result["residual_scale_alpha"] = self.alpha
        return result


def alpha_for(weights_json: str | Path, seed: int, fold: int) -> float:
    payload = json.loads(Path(weights_json).read_text(encoding="utf-8-sig"))
    key = f"seed_{int(seed)}_fold_{int(fold)}"
    if key not in payload["alpha_by_checkpoint"]:
        raise KeyError(key)
    return float(payload["alpha_by_checkpoint"][key])

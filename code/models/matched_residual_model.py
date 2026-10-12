from __future__ import annotations

import torch
from torch import nn
import torch.nn.functional as F

from anatomy_model import _soft_pool
from reliability_model import reliability_features


PHENOTYPE_NAMES = (
    "syndesmotic_separation_proxy",
    "fibular_displacement_proxy",
    "rotational_injury_proxy",
    "medial_restraint_proxy",
    "posterior_restraint_proxy",
    "fracture_complexity_proxy",
)


def reverse_reliability_within_views(value: torch.Tensor, ap_count: int) -> torch.Tensor:
    result = value.clone()
    for start, stop in ((0, ap_count), (ap_count, value.shape[1])):
        block = value[:, start:stop]
        order = torch.argsort(block, dim=1)
        target = torch.empty_like(block)
        target.scatter_(1, order, torch.sort(block, dim=1).values.flip(1))
        result[:, start:stop] = target
    return result


def derange_anchors(value: torch.Tensor, ap_count: int) -> torch.Tensor:
    ap = torch.roll(value[:, :ap_count], shifts=1, dims=1)
    lat = torch.roll(value[:, ap_count:], shifts=1, dims=1)
    return torch.cat((ap, lat), 1)


class PHENOTYPEBiomechanicalPhenotype(nn.Module):

    def __init__(self, baseline, teacher, calibrator, residual_limit: float = 0.75):
        super().__init__()
        self.baseline = baseline
        self.teacher = teacher
        self.calibrator = calibrator
        self.residual_limit = float(residual_limit)
        for module in (baseline, teacher, calibrator):
            for parameter in module.parameters():
                parameter.requires_grad_(False)

        channels = int(baseline.encoder.output_channels)
        self.ap_count = len(teacher.AP_POINTS)
        self.lat_count = len(teacher.LAT_POINTS)
        self.anchor_count = self.ap_count + self.lat_count
        phenotype_count = len(PHENOTYPE_NAMES)
        token_dim = channels + 12 + 2 + 3 + 2
        pair_count = self.anchor_count * (self.anchor_count - 1) // 2
        geometry_dim = self.anchor_count * 5 + pair_count + 2

        self.token_contribution = nn.Sequential(
            nn.LayerNorm(token_dim), nn.Linear(token_dim, 128), nn.GELU(),
            nn.Dropout(0.15), nn.Linear(128, phenotype_count),
        )
        self.geometry_contribution = nn.Sequential(
            nn.LayerNorm(geometry_dim), nn.Linear(geometry_dim, 96), nn.GELU(),
            nn.Dropout(0.10), nn.Linear(96, phenotype_count),
        )
        self.raw_risk_weight = nn.Parameter(torch.zeros(phenotype_count))
        self.risk_bias = nn.Parameter(torch.zeros(()))
        support = torch.tensor([
            [0, 0, 1, 1, 0, 1],  # AP medial malleolus tip
            [1, 1, 1, 0, 0, 1],  # AP fibular tip
            [1, 0, 1, 0, 1, 1],  # AP tibial incisura
            [1, 0, 1, 0, 1, 1],  # AP opposite syndesmotic cortex
            [0, 1, 1, 1, 1, 1],  # AP plafond center
            [0, 1, 1, 1, 1, 1],  # LAT plafond center
            [0, 0, 0, 1, 1, 1],  # LAT medial malleolus tip
            [0, 1, 1, 0, 1, 1],  # LAT fibular tip
        ], dtype=torch.float32)
        if support.shape != (self.anchor_count, phenotype_count):
            raise RuntimeError(
                "The included anatomical support matrix is locked to the audited "
                "8-anchor teacher. A different teacher requires an explicit, reviewed migration."
            )
        self.register_buffer("phenotype_anchor_support", support)

    def _geometry(self, mean, covariance, reliability):
        distances = torch.cdist(mean, mean)
        upper = torch.triu_indices(self.anchor_count, self.anchor_count, 1, device=mean.device)
        pairwise = distances[:, upper[0], upper[1]]
        view_rel = torch.stack(
            (reliability[:, :self.ap_count].mean(1), reliability[:, self.ap_count:].mean(1)), 1
        )
        return torch.cat((mean.flatten(1), covariance.flatten(1), pairwise, view_rel), 1)

    def extract(self, ap: torch.Tensor, lat: torch.Tensor):
        self.baseline.eval(); self.teacher.eval(); self.calibrator.eval()
        with torch.no_grad():
            base = self.baseline(ap, lat)
            anatomy = self.teacher(ap, lat)
            flipped = self.teacher(torch.flip(ap, [-1]), torch.flip(lat, [-1]))
            ap_map = self.baseline.encoder(ap)
            lat_map = self.baseline.encoder(lat)
            aq = reliability_features(anatomy["AP"], flipped["AP"])
            lq = reliability_features(anatomy["LAT"], flipped["LAT"])
            quality = torch.cat((aq, lq), 1)
            reliability = self.calibrator(quality).sigmoid()
            local = torch.cat((
                _soft_pool(ap_map, anatomy["AP"]["probability"]),
                _soft_pool(lat_map, anatomy["LAT"]["probability"]),
            ), 1)
            mean = torch.cat((anatomy["AP"]["mean"], anatomy["LAT"]["mean"]), 1)
            covariance = torch.cat((anatomy["AP"]["covariance"], anatomy["LAT"]["covariance"]), 1)
        view_code = torch.zeros(local.shape[0], self.anchor_count, 2, device=local.device, dtype=local.dtype)
        view_code[:, :self.ap_count, 0] = 1
        view_code[:, self.ap_count:, 1] = 1
        return {
            "base": base, "anatomy": anatomy, "quality": quality,
            "reliability": reliability, "local": local, "mean": mean,
            "covariance": covariance, "view_code": view_code,
        }

    def compose(self, extracted, mode: str = "identity", axis: int | None = None):
        valid = {"identity", "no_biomechanics", "reverse_reliability", "derange_anchors", "zero_axis"}
        if mode not in valid:
            raise ValueError(f"unknown intervention: {mode}")
        reliability = extracted["reliability"]
        local = extracted["local"]
        mean = extracted["mean"]
        covariance = extracted["covariance"]
        quality = extracted["quality"]
        if mode == "reverse_reliability":
            reliability = reverse_reliability_within_views(reliability, self.ap_count)
        elif mode == "derange_anchors":
            local = derange_anchors(local, self.ap_count)

        token = torch.cat((local, quality, mean, covariance, extracted["view_code"]), -1)
        anchor_contribution = self.token_contribution(token) * self.phenotype_anchor_support.unsqueeze(0)
        weighted_anchor = anchor_contribution * reliability.unsqueeze(-1)
        token_term = weighted_anchor.sum(1) / reliability.sum(1, keepdim=True).clamp_min(1e-6)
        geometry_term = 0.25 * torch.tanh(
            self.geometry_contribution(self._geometry(mean, covariance, reliability))
        )
        phenotype_logit = token_term + geometry_term
        phenotype = phenotype_logit.sigmoid()
        if mode == "no_biomechanics":
            phenotype = torch.full_like(phenotype, 0.5)
        elif mode == "zero_axis":
            if axis is None or not 0 <= axis < phenotype.shape[1]:
                raise ValueError("zero_axis requires a valid axis")
            phenotype = phenotype.clone(); phenotype[:, axis] = 0.5

        ap_rel = extracted["reliability"][:, :self.ap_count].mean(1)
        lat_rel = extracted["reliability"][:, self.ap_count:].mean(1)
        gate = 2 * ap_rel * lat_rel / (ap_rel + lat_rel).clamp_min(1e-6)
        risk_weight = F.softplus(self.raw_risk_weight)
        risk_weight = risk_weight / risk_weight.sum().clamp_min(1e-6)
        raw = torch.tanh(((phenotype - 0.5) * risk_weight).sum(1) * len(PHENOTYPE_NAMES) + self.risk_bias)
        delta = self.residual_limit * gate * raw
        base_logit = extracted["base"]["logit"]
        return {
            "logit": base_logit + delta, "baseline_logit": base_logit,
            "biomechanical_residual": delta, "raw_biomechanical_residual": raw,
            "anatomy_gate": gate, "phenotype": phenotype,
            "phenotype_logit": phenotype_logit, "anchor_contribution": anchor_contribution,
            "weighted_anchor_contribution": weighted_anchor,
            "geometry_contribution": geometry_term, "risk_weight": risk_weight,
            "anchor_reliability": reliability, "anatomy": extracted["anatomy"],
        }

    def forward(self, ap, lat, mode: str = "identity", axis: int | None = None):
        return self.compose(self.extract(ap, lat), mode, axis)


def phenotype_loss(output, label, trust_weight=0.10, diversity_weight=0.03, sparse_weight=0.002):
    classification = F.binary_cross_entropy_with_logits(output["logit"], label.float())
    trust = ((1 - output["anatomy_gate"].detach()) * output["biomechanical_residual"]).square().mean()
    phenotype = output["phenotype"]
    centered = phenotype - phenotype.mean(0, keepdim=True)
    covariance = centered.T @ centered / max(1, phenotype.shape[0] - 1)
    off_diagonal = covariance - torch.diag(torch.diagonal(covariance))
    diversity = off_diagonal.square().mean() + F.relu(0.02 - torch.diagonal(covariance)).mean()
    sparse = output["weighted_anchor_contribution"].abs().mean()
    total = classification + trust_weight * trust + diversity_weight * diversity + sparse_weight * sparse
    return total, {"classification": classification.detach(), "trust": trust.detach(), "diversity": diversity.detach(), "sparse": sparse.detach()}

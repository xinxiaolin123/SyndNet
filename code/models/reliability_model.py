from __future__ import annotations
import torch
from torch import nn


def reliability_features(view, flipped_view=None):
    vis=view["visibility_probability"]
    q=view["quality_probability"].unsqueeze(1).expand(-1,vis.shape[1],-1)
    parts=[vis,view["covariance"],view["entropy"].unsqueeze(-1),view["peak"].unsqueeze(-1),q]
    if flipped_view is None: eq=torch.zeros_like(view["entropy"])
    else:
        fm=flipped_view["mean"].clone(); fm[...,0]=1.0-fm[...,0]
        eq=(view["mean"]-fm).square().sum(-1).sqrt()
    parts.append(eq.unsqueeze(-1))
    return torch.cat(parts,-1)


class ReliabilityCalibrator(nn.Module):
    def __init__(self,mean=None,scale=None):
        super().__init__(); self.register_buffer("mean",torch.zeros(12) if mean is None else torch.as_tensor(mean).float()); self.register_buffer("scale",torch.ones(12) if scale is None else torch.as_tensor(scale).float())
        self.net=nn.Sequential(nn.Linear(12,24),nn.GELU(),nn.Dropout(.10),nn.Linear(24,1))
    def forward(self,x): return self.net((x-self.mean)/self.scale.clamp_min(1e-5)).squeeze(-1)

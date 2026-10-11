from __future__ import annotations
import torch
from torch import nn
import torch.nn.functional as F


class ConvNeXtTinyEncoder(nn.Module):
    def __init__(self, pretrained=False):
        super().__init__(); from torchvision.models import ConvNeXt_Tiny_Weights,convnext_tiny
        self.features=convnext_tiny(weights=ConvNeXt_Tiny_Weights.IMAGENET1K_V1 if pretrained else None).features; self.output_channels=768
    def forward(self,image): return self.features(image)


class AttentionPool(nn.Module):
    def __init__(self,channels): super().__init__(); self.score=nn.Conv2d(channels,1,1)
    def forward(self,feature):
        weight=self.score(feature).flatten(2).softmax(-1).view(feature.shape[0],1,feature.shape[2],feature.shape[3]); descriptor=(feature*weight).sum((2,3))
        entropy=-(weight.clamp_min(1e-8).log()*weight).flatten(1).sum(1)/torch.log(torch.tensor(float(feature.shape[2]*feature.shape[3]),device=feature.device))
        return descriptor,entropy


class DIAGNOSTICDualViewModel(nn.Module):
    def __init__(self,encoder,prototype_mean=None,prototype_scale=None):
        super().__init__(); channels=int(encoder.output_channels); self.encoder=encoder
        self.ap_adapter=nn.Sequential(nn.LayerNorm(channels),nn.Linear(channels,channels),nn.GELU()); self.lat_adapter=nn.Sequential(nn.LayerNorm(channels),nn.Linear(channels,channels),nn.GELU())
        self.ap_attention=AttentionPool(channels); self.lat_attention=AttentionPool(channels)
        self.register_buffer("prototype_mean",torch.zeros(2,channels) if prototype_mean is None else prototype_mean.float())
        self.register_buffer("prototype_scale",torch.ones(2,channels) if prototype_scale is None else prototype_scale.float().clamp_min(1e-3))
        fusion_dim=channels*6+4
        self.classifier=nn.Sequential(nn.LayerNorm(fusion_dim),nn.Linear(fusion_dim,512),nn.GELU(),nn.Dropout(.30),nn.Linear(512,128),nn.GELU(),nn.Dropout(.15),nn.Linear(128,1))
    def forward(self,ap,lat):
        am,lm=self.encoder(ap),self.encoder(lat); ag,lg=F.adaptive_avg_pool2d(am,1).flatten(1),F.adaptive_avg_pool2d(lm,1).flatten(1)
        al,ae=self.ap_attention(am); ll,le=self.lat_attention(lm); av,lv=self.ap_adapter(ag),self.lat_adapter(lg)
        anomaly=torch.stack((((ag-self.prototype_mean[0])/self.prototype_scale[0]).square().mean(1),((lg-self.prototype_mean[1])/self.prototype_scale[1]).square().mean(1)),1)
        reliability=torch.stack((ae,le),1); fusion=torch.cat((av,lv,al,ll,(av-lv).abs(),av*lv,anomaly,reliability),1)
        return {"logit":self.classifier(fusion).squeeze(1),"anomaly":anomaly,"attention_entropy":reliability,"embedding":torch.cat((ag,lg),1)}

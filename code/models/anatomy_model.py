from __future__ import annotations
import math,torch
from torch import nn
import torch.nn.functional as F


def distributional_landmarks(logits):
    b,k,h,w=logits.shape; prob=logits.flatten(2).softmax(-1).view(b,k,h,w)
    yy=torch.linspace(0,1,h,device=logits.device,dtype=logits.dtype); xx=torch.linspace(0,1,w,device=logits.device,dtype=logits.dtype); yy,xx=torch.meshgrid(yy,xx,indexing="ij")
    mx=(prob*xx).sum((2,3)); my=(prob*yy).sum((2,3)); dx=xx[None,None]-mx[:,:,None,None]; dy=yy[None,None]-my[:,:,None,None]
    vx=(prob*dx.square()).sum((2,3)); vy=(prob*dy.square()).sum((2,3)); cxy=(prob*dx*dy).sum((2,3)); entropy=-(prob.clamp_min(1e-8).log()*prob).sum((2,3))/math.log(h*w)
    return {"probability":prob,"mean":torch.stack((mx,my),-1),"covariance":torch.stack((vx,cxy,vy),-1),"entropy":entropy,"peak":prob.flatten(2).amax(-1)}


class ConvBlock(nn.Module):
    def __init__(self,cin,cout):
        super().__init__(); self.net=nn.Sequential(nn.Conv2d(cin,cout,3,padding=1,bias=False),nn.GroupNorm(min(16,cout),cout),nn.GELU(),nn.Conv2d(cout,cout,3,padding=1,bias=False),nn.GroupNorm(min(16,cout),cout),nn.GELU())
    def forward(self,x): return self.net(x)


class ConvNeXtAnatomyEncoder(nn.Module):
    def __init__(self,pretrained=False):
        super().__init__(); from torchvision.models import ConvNeXt_Tiny_Weights,convnext_tiny
        model=convnext_tiny(weights=ConvNeXt_Tiny_Weights.IMAGENET1K_V1 if pretrained else None); self.features=nn.Sequential(*list(model.features.children())[:6]); self.output_channels=384
    def forward(self,x): return self.features(x)


class ProbabilisticAnatomyHead(nn.Module):
    def __init__(self,channels,points,hidden=192):
        super().__init__(); self.points=points; self.trunk=ConvBlock(channels,hidden); self.heatmap=nn.Conv2d(hidden,points,1); self.roi=nn.Conv2d(hidden,1,1)
        self.visibility=nn.Sequential(nn.AdaptiveAvgPool2d(1),nn.Flatten(),nn.Linear(hidden,hidden//2),nn.GELU(),nn.Linear(hidden//2,points*3)); self.view_quality=nn.Sequential(nn.AdaptiveAvgPool2d(1),nn.Flatten(),nn.Linear(hidden,3))
    def forward(self,feature):
        z=self.trunk(feature); d=distributional_landmarks(self.heatmap(z)); d["visibility_logits"]=self.visibility(z).view(-1,self.points,3); d["visibility_probability"]=d["visibility_logits"].softmax(-1); d["quality_logits"]=self.view_quality(z); d["quality_probability"]=d["quality_logits"].softmax(-1); d["roi_logits"]=self.roi(z); d["roi_probability"]=d["roi_logits"].sigmoid(); d["feature"]=z; return d


class ANATOMYAnatomyTeacher(nn.Module):
    AP_POINTS=("AP_MM_TIP","AP_FIB_TIP","AP_INCISURA_TIBIAL","AP_SYND_OPPOSITE_CORTEX","AP_PLAFOND_CENTER")
    LAT_POINTS=("LAT_PLAFOND_CENTER","LAT_MM_TIP","LAT_FIB_TIP")
    def __init__(self,encoder):
        super().__init__(); self.encoder=encoder; c=int(encoder.output_channels); self.ap=ProbabilisticAnatomyHead(c,len(self.AP_POINTS)); self.lat=ProbabilisticAnatomyHead(c,len(self.LAT_POINTS))
    def forward(self,ap,lat): return {"AP":self.ap(self.encoder(ap)),"LAT":self.lat(self.encoder(lat))}


def _soft_pool(feature,probability):
    p=F.interpolate(probability,feature.shape[-2:],mode="bilinear",align_corners=False); p=p/p.sum((2,3),keepdim=True).clamp_min(1e-6); return torch.einsum("bkhw,bchw->bkc",p,feature)

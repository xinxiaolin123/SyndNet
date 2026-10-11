import torch
from torch import nn
from torchvision.models import resnet50,ResNet50_Weights

def build_image_only(pretrained=True):
 class Model(nn.Module):
  def __init__(self):
   super().__init__(); w=ResNet50_Weights.IMAGENET1K_V2 if pretrained else None
   self.ap=resnet50(weights=w); self.lat=resnet50(weights=w); d=self.ap.fc.in_features
   self.ap.fc=nn.Identity();self.lat.fc=nn.Identity();self.head=nn.Sequential(nn.LayerNorm(2*d),nn.Dropout(.2),nn.Linear(2*d,1))
  def forward(self,ap,lat): return self.head(torch.cat((self.ap(ap),self.lat(lat)),1)).squeeze(1)
 return Model()

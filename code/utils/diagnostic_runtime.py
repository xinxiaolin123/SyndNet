from __future__ import annotations
import csv,random
from pathlib import Path
from PIL import Image,ImageEnhance,ImageFilter
import torch
from torch.utils.data import Dataset
from torchvision.transforms import functional as TF
from torchvision.transforms import InterpolationMode

MEAN=[.485,.456,.406]; STD=[.229,.224,.225]
def load_manifest(path,expected_cohort):
    rows=list(csv.DictReader(Path(path).open("r",encoding="utf-8-sig",newline="")))
    if not rows or any(r.get("cohort")!=expected_cohort for r in rows): raise RuntimeError(f"manifest is not exclusively {expected_cohort}")
    for row in rows:
        for key in ("ap_path","lat_path"):
            if not Path(row[key]).is_file(): raise FileNotFoundError(row[key])
    return rows
def _pad_square(image):
    w,h=image.size; side=max(w,h); canvas=Image.new("L",(side,side),color=0); canvas.paste(image,((side-w)//2,(side-h)//2)); return canvas
def open_clean(path,size):
    with Image.open(path) as source: image=source.convert("L")
    w,h=image.size; dx,dy=max(1,int(w*.025)),max(1,int(h*.025)); return _pad_square(image.crop((dx,dy,w-dx,h-dy))).resize((size,size),Image.Resampling.BILINEAR).convert("RGB")
def augment(image,strong):
    if random.random()<.5: image=TF.hflip(image)
    image=TF.affine(image,random.uniform(-5,5),[int(random.uniform(-.03,.03)*image.width),int(random.uniform(-.03,.03)*image.height)],random.uniform(.96,1.04),0,interpolation=InterpolationMode.BILINEAR,fill=0)
    image=ImageEnhance.Contrast(image).enhance(random.uniform(.82 if strong else .92,1.18 if strong else 1.08)); image=ImageEnhance.Brightness(image).enhance(random.uniform(.88 if strong else .96,1.12 if strong else 1.04))
    if strong and random.random()<.25: image=image.filter(ImageFilter.GaussianBlur(random.uniform(.1,1)))
    return TF.normalize(TF.to_tensor(image),MEAN,STD)
def clean_tensor(path,size): return TF.normalize(TF.to_tensor(open_clean(path,size)),MEAN,STD)
class ClassificationDataset(Dataset):
    def __init__(self,rows,size,train): self.rows,self.size,self.train=rows,size,train
    def __len__(self): return len(self.rows)
    def __getitem__(self,index):
        row=self.rows[index]; ap=augment(open_clean(row["ap_path"],self.size),True) if self.train else clean_tensor(row["ap_path"],self.size); lat=augment(open_clean(row["lat_path"],self.size),True) if self.train else clean_tensor(row["lat_path"],self.size)
        raw=row.get("label",""); label=-1. if raw in ("",None,"None") else float(raw)
        return {"release_case_id":row["release_case_id"],"ap":ap,"lat":lat,"label":torch.tensor(label),"center":row["center"],"fold":row.get("fold","")}

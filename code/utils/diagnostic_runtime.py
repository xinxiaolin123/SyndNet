from PIL import Image
from torchvision.transforms import functional as TF

MEAN=[.485,.456,.406]; STD=[.229,.224,.225]
def _pad_square(image):
    w,h=image.size; side=max(w,h); canvas=Image.new("L",(side,side),color=0); canvas.paste(image,((side-w)//2,(side-h)//2)); return canvas
def open_clean(path,size):
    with Image.open(path) as source: image=source.convert("L")
    w,h=image.size; dx,dy=max(1,int(w*.025)),max(1,int(h*.025)); return _pad_square(image.crop((dx,dy,w-dx,h-dy))).resize((size,size),Image.Resampling.BILINEAR).convert("RGB")
def clean_tensor(path,size): return TF.normalize(TF.to_tensor(open_clean(path,size)),MEAN,STD)

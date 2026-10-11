"""Generate two nonclinical grayscale test patterns; no diagnostic meaning."""
from pathlib import Path
import argparse
from PIL import Image
import numpy as np
def main():
    p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
    a.output_dir.mkdir(parents=True,exist_ok=True)
    yy,xx=np.indices((448,320))
    for name,data in [('AP',(xx+2*yy)%256),('LAT',(3*xx+yy)%256)]:
        Image.fromarray(data.astype('uint8')).save(a.output_dir/(name+'.png'))
if __name__=='__main__':main()

"""Use the released original deterministic preprocessing without modification."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code/utils'))
from diagnostic_runtime import clean_tensor

def paired_tensors(ap,lat,size=384):
    if size!=384:raise ValueError('Locked inference resolution is 384')
    return clean_tensor(str(ap),size).unsqueeze(0),clean_tensor(str(lat),size).unsqueeze(0)

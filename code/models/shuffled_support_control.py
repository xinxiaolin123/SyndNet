import hashlib,json,random
from pathlib import Path
import torch

def degree_preserving_support(original,seed):
 x=original.detach().cpu().clone(); rng=random.Random(790100+int(seed)); rows,cols=x.shape; swaps=0
 for _ in range(20000):
  a,b=rng.sample(range(rows),2); c,d=rng.sample(range(cols),2)
  if x[a,c]==1 and x[b,d]==1 and x[a,d]==0 and x[b,c]==0:
   x[a,c]=x[b,d]=0;x[a,d]=x[b,c]=1;swaps+=1
  elif x[a,d]==1 and x[b,c]==1 and x[a,c]==0 and x[b,d]==0:
   x[a,d]=x[b,c]=0;x[a,c]=x[b,d]=1;swaps+=1
  if swaps>=64: break
 if swaps<8 or torch.equal(x,original.cpu()): raise RuntimeError("unable to create nontrivial degree-preserving support")
 if not torch.equal(x.sum(0),original.cpu().sum(0)) or not torch.equal(x.sum(1),original.cpu().sum(1)): raise RuntimeError("degree contract failed")
 return x,swaps

def install_shuffled_support(model,seed,audit_path=None):
 old=model.phenotype_anchor_support.detach().cpu(); new,swaps=degree_preserving_support(old,seed)
 model.phenotype_anchor_support.copy_(new.to(model.phenotype_anchor_support))
 payload={"protocol":"DEGREE-PRESERVING-SUPPORT-1.0","seed":int(seed),"successful_switches":swaps,"original":old.int().tolist(),"shuffled":new.int().tolist(),"row_degrees":new.sum(1).int().tolist(),"column_degrees":new.sum(0).int().tolist(),"sha256":hashlib.sha256(new.numpy().tobytes()).hexdigest()}
 if audit_path: Path(audit_path).write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
 return model


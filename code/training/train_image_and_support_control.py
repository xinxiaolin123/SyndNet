from __future__ import annotations
import argparse,csv,json,random,sys
from pathlib import Path
import numpy as np,torch
from torch.utils.data import DataLoader

def loader(rows,size,train,batch,workers,seed):
 from diagnostic_runtime import ClassificationDataset
 g=torch.Generator().manual_seed(seed)
 return DataLoader(ClassificationDataset(rows,size,train),batch_size=batch,shuffle=train,num_workers=workers,pin_memory=True,drop_last=train,generator=g if train else None)

def main():
 p=argparse.ArgumentParser();p.add_argument('--arm',choices=['image_only','shuffled_support'],required=True);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--seed',type=int,required=True);p.add_argument('--fold',type=int,required=True);p.add_argument('--image-size',type=int,default=384);p.add_argument('--workers',type=int,default=4);p.add_argument('--epochs',type=int,default=30);p.add_argument('--phenotype-root',type=Path);p.add_argument('--frozen-root',type=Path);a=p.parse_args()
 sys.path.insert(0,str(a.phenotype_root/'src'));from diagnostic_runtime import load_manifest
 random.seed(a.seed+a.fold);np.random.seed(a.seed+a.fold);torch.manual_seed(a.seed+a.fold);torch.cuda.manual_seed_all(a.seed+a.fold)
 rows=load_manifest(a.manifest,'internal');tr=[r for r in rows if int(r['fold'])!=a.fold];te=[r for r in rows if int(r['fold'])==a.fold];a.output.mkdir(parents=True,exist_ok=True)
 if all((a.output/x).is_file() for x in ('COMPLETE','model.pt','predictions.csv')): print('SKIP_COMPLETE');return
 if a.arm=='image_only':
  from image_only_model import build_image_only; model=build_image_only(True).cuda();params=list(model.parameters());lr=1e-4;wd=1e-4;batch=2;accum=8
 else:
  from phenotype_common import init_model;from shuffled_support_control import install_shuffled_support
  model=init_model(a.frozen_root/'normal'/'DIAGNOSTIC_NORMAL_SSL.pt',a.frozen_root/'baseline'/f'fold_{a.fold}'/'model.pt',a.frozen_root/'teacher_oof'/f'fold_{a.fold}'/'best.pt',a.frozen_root/'calibrators'/f'fold_{a.fold}.pt');install_shuffled_support(model,a.seed,a.output/'SUPPORT_AUDIT.json');model=model.cuda();params=[x for x in model.parameters() if x.requires_grad];lr=2e-4;wd=.03;batch=4;accum=4
 opt=torch.optim.AdamW(params,lr=lr,weight_decay=wd);sc=torch.amp.GradScaler('cuda');last=a.output/'last.pt';start=0
 if last.exists():
  s=torch.load(last,map_location='cpu',weights_only=False);model.load_state_dict(s['model'],strict=True);opt.load_state_dict(s['optimizer']);start=s['epoch']+1
 for ep in range(start,a.epochs):
  model.train(); losses=[];opt.zero_grad(set_to_none=True)
  if a.arm=='shuffled_support': model.baseline.eval();model.teacher.eval();model.calibrator.eval()
  train_loader=loader(tr,a.image_size,True,batch,a.workers,a.seed*10000+a.fold*100+ep)
  for i,b in enumerate(train_loader,1):
   y=b['label'].cuda(non_blocking=True).float()
   with torch.autocast('cuda',dtype=torch.float16):
    if a.arm=='image_only': logit=model(b['ap'].cuda(non_blocking=True),b['lat'].cuda(non_blocking=True));loss=torch.nn.functional.binary_cross_entropy_with_logits(logit,y)
    else:
     from matched_residual_model import phenotype_loss;out=model(b['ap'].cuda(non_blocking=True),b['lat'].cuda(non_blocking=True));loss=phenotype_loss(out,y)[0]
    z=loss/accum
   sc.scale(z).backward();losses.append(float(loss.detach()))
   if i%accum==0 or i==len(train_loader): sc.unscale_(opt);torch.nn.utils.clip_grad_norm_(params,3);sc.step(opt);sc.update();opt.zero_grad(set_to_none=True)
  torch.save({'model':model.state_dict(),'optimizer':opt.state_dict(),'epoch':ep,'arm':a.arm,'seed':a.seed,'fold':a.fold},last);print(json.dumps({'event':'CONTROL_EPOCH','arm':a.arm,'seed':a.seed,'fold':a.fold,'epoch':ep,'loss':np.mean(losses)}),flush=True)
 rec=[];model.eval()
 with torch.inference_mode():
  for b in loader(te,a.image_size,False,4,a.workers,0):
   with torch.autocast('cuda',dtype=torch.float16):
    logit=model(b['ap'].cuda(),b['lat'].cuda()) if a.arm=='image_only' else model(b['ap'].cuda(),b['lat'].cuda())['logit']
   prob=logit.float().sigmoid().cpu().numpy()
   for i,k in enumerate(b['release_case_id']):rec.append({'release_case_id':k,'center':b['center'][i],'label':int(b['label'][i]),'seed':a.seed,'fold':a.fold,'probability':float(prob[i])})
 with (a.output/'predictions.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rec[0]);w.writeheader();w.writerows(rec)
 torch.save({'protocol':'CONTROL-'+a.arm.upper()+'-FINAL-1.0','state_dict':model.state_dict(),'seed':a.seed,'fold':a.fold},a.output/'model.pt');(a.output/'COMPLETE').write_text('COMPLETE\n');print(json.dumps({'status':'FOLD_COMPLETE','arm':a.arm,'seed':a.seed,'fold':a.fold,'n':len(rec)}))
if __name__=='__main__':main()

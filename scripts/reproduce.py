"""Reproduce frozen performance estimates from released derived predictions."""
from pathlib import Path
import argparse,json,os
import numpy as np,pandas as pd
from sklearn.metrics import roc_auc_score,average_precision_score
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent / "code" / "bootstrap"))
from bootstrap_core import patient_weights,weighted_metrics,METRICS
ROOT=Path(__file__).resolve().parents[1]
DATA_ROOT=Path(os.environ.get('SYNDNET_ANALYSIS_DATA_DIR',str(ROOT/'data')))
REFERENCE_ROOT=Path(os.environ.get('SYNDNET_ANALYSIS_REFERENCE_DIR',str(ROOT/'results')))
READER_RESULTS_ROOT=Path(os.environ.get('SYNDNET_READER_RESULTS_DIR',str(ROOT/'reader_study_reproducibility'/'controlled_results')))
OUTPUT_ROOT=Path(os.environ.get('SYNDNET_ANALYSIS_OUTPUT_DIR',str(ROOT/'reproduction_output')))


def read(name):
 path=DATA_ROOT/name
 if not path.is_file():raise FileNotFoundError('Study input '+name+' is controlled. Set SYNDNET_ANALYSIS_DATA_DIR to an approved external directory; see DATA_ACCESS.md.')
 if path.resolve().is_relative_to(ROOT.resolve()):raise ValueError('Controlled study inputs must be outside the public repository.')
 return pd.read_csv(path,float_precision='round_trip')
def metric(d):
 y=d.reference_label.to_numpy(dtype=int);p=d.predicted_probability.to_numpy(dtype=float);q=d.fixed_prediction.to_numpy(dtype=bool)
 return dict(zip(METRICS,weighted_metrics(y,p,q,np.ones((1,len(d)),int))[0]))
def reproduce(target):
 result=[]
 if target=='table3':
  df=read('ablation_patient_predictions.csv')
  for name,d in df.groupby('model',sort=False):
   ss=[metric(g) for _,g in d.groupby('seed',sort=True)];result.append(dict(table='Table3',model=name,**{k:float(np.mean([r[k] for r in ss])) for k in METRICS}))
 elif target=='table2':
  df=read('final_model_predictions.csv')
  for cohort,d in df.groupby('cohort',sort=False):result.append(dict(table='Table2',cohort=cohort,**metric(d)))
  d=df[df.cohort!='Internal OOF'];result.append(dict(table='Table2',cohort='Pooled external validation',**metric(d)))
 else:result.append(dict(table='Table4',cohort='Reader-study cases',**metric(read('reader_study_model_predictions.csv'))))
 return result

def run(target):
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=OUTPUT_ROOT/('reproduced_'+target+'.csv'));args=parser.parse_args()
 rows=reproduce(target);expected=json.loads((ROOT/'configs/expected_points.json').read_text())[target]
 for row,ref in zip(rows,expected):
  for key in METRICS:
   if key in ref and abs(row[key]-ref[key])>1e-10:raise RuntimeError('POINT ESTIMATE PROVENANCE FAILURE: '+str((row,key,row[key],ref[key])))
 assert len(rows)==len(expected);args.output.parent.mkdir(parents=True,exist_ok=True);pd.DataFrame(rows).to_csv(args.output,index=False,float_format='%.17g',encoding='utf-8',lineterminator='\n');print('Reproduced '+target+': '+str(len(rows))+' rows')

def run_bootstrap():
 parser=argparse.ArgumentParser(description='Patient bootstrap with frozen predictions and thresholds');parser.add_argument('--output',type=Path,default=OUTPUT_ROOT/'reproduced_bootstrap_ci.csv');args=parser.parse_args();cfg=json.loads((ROOT/'configs/statistical_config.json').read_text());rows=[]
 df=read('ablation_patient_predictions.csv');names=df.model.drop_duplicates().tolist();seeds=[42,123,456];first=df[(df.model==names[0])&(df.seed==42)];y=first.reference_label.to_numpy(dtype=int);fold=first.fold.to_numpy();ids=first.release_case_id.tolist();w=patient_weights(y,fold,10000,cfg['ablation_seed']);ensembles={}
 for name in names:
  samples=[];ps=[]
  for seed in seeds:
   d=df[(df.model==name)&(df.seed==seed)];assert d.release_case_id.tolist()==ids and np.array_equal(d.reference_label,y)
   p=d.predicted_probability.to_numpy();q=d.fixed_prediction.to_numpy(dtype=bool);samples.append(weighted_metrics(y,p,q,w));ps.append(p)
  ensembles[name]=np.mean(ps,axis=0);s=np.mean(samples,axis=0)
  for key in ['AUROC','AP','Specificity','FP']:
   j=METRICS.index(key);lo,hi=np.quantile(s[:,j],[.025,.975]);rows.append(dict(table='Table3',cohort='Internal OOF',model=name,metric=key,ci_low=lo,ci_high=hi))
 for ref in ['Permuted patient-specific correspondence','Parameter-matched shuffled anatomical support prior']:
  a=weighted_metrics(y,ensembles['Final SyndNet'],ensembles['Final SyndNet']>=.5,w)[:,0];b=weighted_metrics(y,ensembles[ref],ensembles[ref]>=.5,w)[:,0];lo,hi=np.quantile(a-b,[.025,.975]);rows.append(dict(table='Table3',cohort='Internal OOF',model='Final SyndNet – '+ref,metric='ΔAUROC',ci_low=lo,ci_high=hi))
 rng=np.random.default_rng(cfg['matched_effect_seed']);repseeds=rng.integers(0,2**32-1,size=10000,dtype=np.uint32);oldw=np.zeros_like(w);pos=np.flatnonzero(y==1);neg=np.flatnonzero(y==0)
 for b,seed in enumerate(repseeds):
  rg=np.random.default_rng(int(seed));ix=np.r_[rg.choice(pos,len(pos),True),rg.choice(neg,len(neg),True)];rg.shuffle(ix);oldw[b]=np.bincount(ix,minlength=len(y))
 a=weighted_metrics(y,ensembles['Matched residual'],ensembles['Matched residual']>=.5,oldw)[:,0];b=weighted_metrics(y,ensembles['Without residual'],ensembles['Without residual']>=.5,oldw)[:,0];lo,hi=np.quantile(a-b,[.025,.975]);rows.append(dict(table='Table3',cohort='Internal OOF',model='Matched residual – Without residual',metric='ΔAUROC',ci_low=lo,ci_high=hi))
 df=read('final_model_predictions.csv');groups=list(df.groupby('cohort',sort=False));groups.append(('Pooled external validation',df[df.cohort!='Internal OOF']))
 for i,(cohort,d) in enumerate(groups):
  yy=d.reference_label.to_numpy(dtype=int);p=d.predicted_probability.to_numpy();q=d.fixed_prediction.to_numpy(dtype=bool);blocks=d.fold.to_numpy() if i==0 else d.centre.to_numpy();ww=patient_weights(yy,blocks,10000,cfg['table2_seed_base']+i);s=weighted_metrics(yy,p,q,ww)
  for key in ['AP','Sensitivity','Specificity','Accuracy']:
   lo,hi=np.quantile(s[:,METRICS.index(key)],[.025,.975])
   if cohort=='Center 3' and key=='Sensitivity':lo,hi=cfg['centre3_boundary_sensitivity_ci']
   rows.append(dict(table='Table2',cohort=cohort,model='Final SyndNet',metric=key,ci_low=lo,ci_high=hi))
 d=read('reader_study_model_predictions.csv');yy=d.reference_label.to_numpy(dtype=int);p=d.predicted_probability.to_numpy();q=d.fixed_prediction.to_numpy(dtype=bool)
 rng=np.random.default_rng(cfg['table4_seed']);pos=np.flatnonzero(yy==1);neg=np.flatnonzero(yy==0);ww=np.zeros((10000,len(yy)),np.int16)
 for b in range(10000):
  ix=np.r_[rng.choice(pos,len(pos),replace=True),rng.choice(neg,len(neg),replace=True)];ww[b]=np.bincount(ix,minlength=len(yy))
 s=weighted_metrics(yy,p,q,ww)
 for key in ['AUROC','Sensitivity','Specificity','Accuracy']:
  lo,hi=np.quantile(s[:,METRICS.index(key)],[.025,.975]);rows.append(dict(table='Table4',cohort='Reader-study cases',model='Final SyndNet',metric=key,ci_low=lo,ci_high=hi))
 args.output.parent.mkdir(parents=True,exist_ok=True);pd.DataFrame(rows).to_csv(args.output,index=False,float_format='%.17g',encoding='utf-8',lineterminator='\n');print('Reproduced bootstrap: '+str(len(rows))+' intervals')

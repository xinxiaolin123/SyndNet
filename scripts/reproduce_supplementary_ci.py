"""Reproduce supplementary discrimination intervals and export R individual-reader intervals."""
import json
from pathlib import Path
import numpy as np,pandas as pd
from reproduce import ROOT,read,REFERENCE_ROOT,READER_RESULTS_ROOT,OUTPUT_ROOT
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent / "code" / "bootstrap"))
from bootstrap_core import patient_weights,weighted_metrics

if OUTPUT_ROOT.resolve().is_relative_to(ROOT.resolve()):
 raise ValueError('Set SYNDNET_ANALYSIS_OUTPUT_DIR to an external controlled output directory for individual-reader intervals.')
if READER_RESULTS_ROOT.resolve().is_relative_to(ROOT.resolve()):
 raise ValueError('Set SYNDNET_READER_RESULTS_DIR to the external approved reader-study results.')

expected=pd.read_csv(REFERENCE_ROOT/'supplementary_ci.csv',float_precision='round_trip')
pred=read('supplementary_discrimination_predictions.csv');out=[]
for (name,cohort),d in pred.groupby(['model','cohort'],sort=False):
 refs=expected[(expected.model==name)&(expected.cohort==cohort)]
 if name=='Final SyndNet':
  # These are identical to the main-table estimand and retain its authoritative intervals.
  for r in refs.to_dict('records'):out.append(dict(r,reproduction='identical main-table estimand; authoritative interval retained'))
  continue
 streams=[]
 for seed,g in d.groupby('seed',sort=False):
  yy=g.reference_label.to_numpy(dtype=int);p=g.predicted_probability.to_numpy();blocks=g.fold.to_numpy() if cohort=='Internal OOF' else g.centre.to_numpy()
  bseed=2026100831 if name=='ImageNet-initialized anatomy teacher' and cohort=='Internal OOF' else 2026100833 if name=='ImageNet-initialized anatomy teacher' else 2026100839
  w=patient_weights(yy,blocks,10000,bseed);streams.append(weighted_metrics(yy,p,p>=.5,w)[:,:2])
 samples=np.mean(streams,axis=0)
 for j,key in enumerate(['AUROC','AP']):
  r=refs[refs.metric==key].iloc[0].to_dict();lo,hi=np.quantile(samples[:,j],[.025,.975]);assert np.allclose([lo,hi],[r['ci_low'],r['ci_high']],rtol=0,atol=1e-10)
  out.append(dict(r,reproduction='patient bootstrap reproduced'))
readers=pd.read_csv(READER_RESULTS_ROOT/'reader_paired_bootstrap.csv',float_precision='round_trip')
for reader in readers.to_dict('records'):
 for key,condition in [('Unaided AUROC','unaided'),('Assisted AUROC','assisted'),('ΔAUROC','difference')]:
  r=expected[(expected.model==reader['reader_id'])&(expected.metric==key)].iloc[0].to_dict()
  r['ci_low']=reader[condition+'_low'];r['ci_high']=reader[condition+'_high']
  r['ci_method']='Paired reference-class-stratified case bootstrap'
  out.append(dict(r,reproduction='R individual-reader bootstrap interval'))
assert len(out)==len(expected)
OUTPUT_ROOT.mkdir(parents=True,exist_ok=True)
pd.DataFrame(out).to_csv(OUTPUT_ROOT/'reproduced_supplementary_ci.csv',index=False,float_format='%.17g',encoding='utf-8',lineterminator='\n')
print('Supplementary intervals checked: '+str(len(out)))

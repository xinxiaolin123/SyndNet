"""Demonstrate the metric interface using four invented, nonclinical observations."""
from pathlib import Path
import csv,json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code/bootstrap'))
from bootstrap_core import weighted_metrics,METRICS
with Path(__file__).with_suffix('.csv').open(newline='') as f:
    rows=list(csv.DictReader(f))
y=np.array([int(r['reference_label']) for r in rows])
p=np.array([float(r['predicted_probability']) for r in rows])
q=np.array([int(r['fixed_prediction']) for r in rows],dtype=bool)
values=weighted_metrics(y,p,q,np.ones((1,len(rows)),dtype=int))[0]
print(json.dumps({'scope':'Invented demonstration only; not SyndNet study data',
                  'metrics':dict(zip(METRICS,values.tolist()))},indent=2))

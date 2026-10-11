"""Deterministic weighted patient bootstrap with fixed classifications."""
import numpy as np

def patient_weights(labels,blocks,replicates,seed):
    labels=np.asarray(labels);blocks=np.asarray(blocks);rng=np.random.default_rng(seed)
    w=np.zeros((replicates,len(labels)),dtype=np.int16)
    for block in np.unique(blocks):
        for label in (0,1):
            ix=np.flatnonzero((blocks==block)&(labels==label))
            if len(ix):
                for start in range(0,replicates,500):
                    stop=min(start+500,replicates)
                    draws=rng.choice(ix,size=(stop-start,len(ix)),replace=True)
                    for j,row in enumerate(draws,start):w[j]+=np.bincount(row,minlength=len(labels)).astype(np.int16)
    return w

def weighted_metrics(labels,probability,decision,weights):
    y=np.asarray(labels,dtype=int);p=np.asarray(probability,dtype=float);q=np.asarray(decision,dtype=bool)
    order=np.argsort(-p,kind='stable');end=np.r_[np.flatnonzero(np.diff(p[order])!=0),len(p)-1]
    start=np.r_[0,end[:-1]+1];out=[]
    for offset in range(0,len(weights),500):
        w=weights[offset:offset+500].astype(float);v=w[:,order]
        pos=np.add.reduceat(v*y[order],start,axis=1);neg=np.add.reduceat(v*(1-y[order]),start,axis=1)
        cp=np.cumsum(pos,axis=1);cn=np.cumsum(neg,axis=1);np_=cp[:,-1];nn=cn[:,-1]
        auc=np.sum(pos*(nn[:,None]-cn+neg*.5),axis=1)/(np_*nn)
        ap=np.sum(pos*cp/np.maximum(cp+cn,1),axis=1)/np_
        tp=w@(q&(y==1));tn=w@(~q&(y==0));fp=w@(q&(y==0))
        out.append(np.column_stack([auc,ap,tp/np_,tn/nn,(tp+tn)/(np_+nn),fp]))
    return np.concatenate(out)

METRICS=['AUROC','AP','Sensitivity','Specificity','Accuracy','FP']

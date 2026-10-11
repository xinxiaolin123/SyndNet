import numpy as np
import torch

def predict_tensors(weights,ap,lat,device='cuda',oof_fold=None):
    """External/new-case ensemble; optional held-out fold only for OOF fidelity."""
    if device!='cuda' or not torch.cuda.is_available():
        raise RuntimeError('This fidelity-verified release requires CUDA float16 autocast')
    singleton=ap.shape[0]==1
    if singleton:
        # Preserve the authoritative external size-4 kernel context for the paired CLI.
        # Copies are independent examinations with identical tensors; return the first.
        ap=ap.repeat(4,1,1,1);lat=lat.repeat(4,1,1,1)
    seed_probabilities=[];modules=[]
    folds=weights.config['folds'] if oof_fold is None else [int(oof_fold)]
    with torch.inference_mode():
        for seed in weights.config['seeds']:
            logits=[]
            for fold in folds:
                model=weights.model(seed,fold,device)
                with torch.autocast('cuda',dtype=torch.float16):out=model(ap.to(device),lat.to(device))
                base=out['baseline_logit'].float().cpu().numpy()
                residual=out['biomechanical_residual'].float().cpu().numpy()
                alpha=weights.config['alpha_by_checkpoint'][f'seed_{seed}_fold_{fold}']
                logits.append(base+alpha*residual)
                modules.append(f'seed_{seed}_fold_{fold}')
                del model,out
            seed_probabilities.append(1/(1+np.exp(-np.stack(logits).mean(0))))
    result=np.mean(np.stack(seed_probabilities),axis=0)
    return result[:1] if singleton else result,modules

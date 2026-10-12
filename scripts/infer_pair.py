"""Run the frozen final SyndNet ensemble on one paired AP/lateral examination."""
from pathlib import Path
import argparse,json,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from inference.loader import LockedWeights
from inference.preprocessing import paired_tensors
from inference.ensemble import predict_tensors

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--ap',type=Path,required=True);p.add_argument('--lat',type=Path,required=True)
    p.add_argument('--weights-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();start=time.perf_counter();weights=LockedWeights(args.weights_dir)
    ap,lat=paired_tensors(args.ap,args.lat);prob,modules=predict_tensors(weights,ap,lat)
    value=float(prob[0]);threshold=weights.config['fixed_threshold']
    result={'final_probability':value,'fixed_threshold':threshold,'predicted_class':int(value>=threshold),'software_version':'1.1.1','model_version':'1.1.0','checkpoint_manifest_hash':weights.manifest_hash,'modules_loaded':modules,'missing_keys':[],'unexpected_keys':[],'inference_device':'cuda','runtime_seconds':time.perf_counter()-start}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()

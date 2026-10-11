from pathlib import Path
import hashlib,json,sys
import torch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code/models'))
from diagnostic_model import ConvNeXtTinyEncoder,DIAGNOSTICDualViewModel
from anatomy_model import ConvNeXtAnatomyEncoder,ANATOMYAnatomyTeacher
from reliability_model import ReliabilityCalibrator
from matched_residual_model import PHENOTYPEBiomechanicalPhenotype

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
    return h.hexdigest()

class LockedWeights:
    def __init__(self,directory):
        self.directory=Path(directory)
        self.manifest_hash=sha256(self.directory/'MANIFEST.json')
        expected=sha256(ROOT/'weights/MANIFEST.json')
        if self.manifest_hash!=expected:raise ValueError('Weight manifest does not match this code release')
        self.manifest=json.loads((self.directory/'MANIFEST.json').read_text())
        self.config=json.loads((self.directory/'inference_config.json').read_text())
        self.graph=json.loads((self.directory/'checkpoint_dependency_graph.json').read_text())['models']
        for name in ['inference_config.json','checkpoint_dependency_graph.json']:
            if sha256(self.directory/name)!=sha256(ROOT/'weights'/name):raise ValueError('Inference configuration mismatch')
        self.states={}
        for entry in self.manifest['files']:
            path=self.directory/entry['file']
            if sha256(path)!=entry['sha256']:raise ValueError('Checkpoint SHA256 mismatch: '+entry['file'])
            state=torch.load(path,map_location='cpu',weights_only=True)
            if not isinstance(state,dict) or not all(isinstance(v,torch.Tensor) for v in state.values()):raise ValueError('Expected tensor-only state dictionary')
            self.states[entry['file']]=state

    def model(self,seed,fold,device):
        entry=next(x for x in self.graph if x['seed']==seed and x['fold']==fold)
        model=PHENOTYPEBiomechanicalPhenotype(DIAGNOSTICDualViewModel(ConvNeXtTinyEncoder(False)),ANATOMYAnatomyTeacher(ConvNeXtAnatomyEncoder(False)),ReliabilityCalibrator())
        state={}
        for family,prefix in [('diagnostic','baseline.'),('anatomy','teacher.'),('reliability','calibrator.'),('residual','')]:
            state.update({prefix+k:v for k,v in self.states[entry['components'][family]].items()})
        model.load_state_dict(state,strict=True)
        return model.to(device).eval()

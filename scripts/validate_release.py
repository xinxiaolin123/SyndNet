"""Check distributed file integrity, checkpoint metadata and public synthetic input formats."""
from pathlib import Path
import csv,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
def validate():
 entries=[]
 for line in (ROOT/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
  digest,name=line.split('  ',1)
  path=(ROOT/name).resolve()
  assert path.is_relative_to(ROOT.resolve()),name
  assert hashlib.sha256(path.read_bytes()).hexdigest()==digest,name
  entries.append(name)
 manifest=json.loads((ROOT/'weights/MANIFEST.json').read_text())
 graph=json.loads((ROOT/'weights/checkpoint_dependency_graph.json').read_text())['models']
 config=json.loads((ROOT/'weights/inference_config.json').read_text())
 assert len(manifest['files'])==30 and len(graph)==15
 names={x['file'] for x in manifest['files']}
 assert len(names)==30
 for item in manifest['files']:
  assert re.fullmatch('[0-9a-f]{64}',item['sha256'])
  assert re.fullmatch('[0-9a-f]{64}',item['canonical_tensor_sha256'])
  assert item['bytes']>0 and item['tensor_count']>0
  assert item['missing_keys']==[] and item['unexpected_keys']==[]
 assert {(x['seed'],x['fold']) for x in graph}=={(s,f) for s in [42,123,456] for f in range(5)}
 assert all(set(x['components'].values())<=names for x in graph)
 assert config['fixed_threshold']==0.012530357984719657
 assert len(config['alpha_by_checkpoint'])==15
 checkpoint_hashes={x['file']:x['sha256'] for x in manifest['files']}
 weight_entries={}
 for line in (ROOT/'weights/SHA256SUMS').read_text().splitlines():
  digest,name=line.split('  ',1)
  assert name not in weight_entries
  weight_entries[name]=digest
  if name in checkpoint_hashes:assert checkpoint_hashes[name]==digest,name
  else:assert hashlib.sha256((ROOT/'weights'/name).read_bytes()).hexdigest()==digest,name
 assert set(checkpoint_hashes)<=set(weight_entries)
 from validate_synthetic_formats import validate_formats
 validate_formats()
 return len(entries)
if __name__=='__main__':print('Verified '+str(validate())+' files, checkpoint metadata and synthetic input formats')

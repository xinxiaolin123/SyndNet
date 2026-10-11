"""Validate preserved scientific payload and structural release integrity."""
from pathlib import Path
import csv,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def validate():
 manifest=json.loads((ROOT/'environments/frozen_payload_manifest.json').read_text(encoding='utf-8'))
 for item in manifest['files']:
  path=manifest['relocations'].get(item['path'],item['path'])
  assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==item['SHA256'],path
 paired=ROOT/'MRMC/01_input/MRMC_REAL_READER_CASE_FINAL.csv'
 with paired.open(encoding='utf-8-sig',newline='') as f:
  rows=list(csv.DictReader(f))
 assert len(rows)==30750
 assert len({r['reader_id'] for r in rows})==15
 assert len({r['case_id'] for r in rows})==2050
 assert len({(r['reader_id'],r['case_id']) for r in rows})==30750
 with (ROOT/'MRMC/01_input/MRMC_REAL_LONG_FINAL.csv').open(encoding='utf-8-sig',newline='') as f:
  assert sum(1 for _ in csv.DictReader(f))==61500
 for filename in ['MRMC_INPUT_QC.csv','MRMC_AUROC_FINGERPRINT_QC.csv','MRMC_POST_ANALYSIS_CHECKS.csv']:
  with (ROOT/'MRMC/04_QC'/filename).open(encoding='utf-8-sig',newline='') as f:
   assert all(r['pass'].upper()=='TRUE' for r in csv.DictReader(f)),filename
 assert '_PRIVATE_REVIEW_DO_NOT_COMMIT/' in (ROOT/'.gitignore').read_text()
 return len(manifest['files'])
if __name__=='__main__':print('PASS: '+str(validate())+' frozen payload files and reader/QC structure')

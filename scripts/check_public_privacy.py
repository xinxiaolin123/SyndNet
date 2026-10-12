"""Check the publication tree for controlled records and machine-specific content."""
from pathlib import Path
import csv,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
def public_files():
 try:
  top=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).strip())
  if top.resolve()==ROOT.resolve():
   return [ROOT/x for x in subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0') if x]
 except (OSError,subprocess.CalledProcessError):pass
 return [p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts]
def check():
 files=public_files()
 listed={line.split('  ',1)[1] for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines()}
 assert {p.relative_to(ROOT).as_posix() for p in files}==listed|{'SHA256SUMS.txt'},'Publication manifest does not cover the full source tree'
 patterns=[r'\b[A-Za-z]:[\\/]',r'/(?:home|mnt|root|Users|private|tmp)/',r'\b(?:CASE\d{6}|R\d{2})\b',r'gh[pousr]_[A-Za-z0-9]{20,}',r'github_pat_[A-Za-z0-9_]{20,}']
 protected={'patient_id','patient_name','accession','accession_number','study_hash','reader_id','case_id','release_case_id','hospital','hospital_name'}
 for p in files:
  name=p.relative_to(ROOT).as_posix()
  assert p.suffix.lower() not in {'.dcm','.dicom','.xlsx','.xls','.rds','.pt','.pth','.ckpt','.png','.jpg','.jpeg'},name
  text=p.read_text(encoding='utf-8-sig')
  if p.name not in {'check_public_privacy.py','check_public_paths.py'}:
   assert not any(re.search(pattern,text) for pattern in patterns),name
   emails=re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',text)
   assert all(email=='2060753088@qq.com' for email in emails),name
  if p.suffix=='.csv':
   with p.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
   if rows and protected&set(rows[0]):
    assert '/examples/' in name,name
    assert all(all(v.startswith('EXAMPLE_') for k,v in row.items() if k in {'reader_id','case_id'}) for row in rows),name
 assert not any((ROOT/x).exists() for x in ['MRMC','reader_study','reader_study_reproducibility/input','reader_study_reproducibility/results','reader_study_reproducibility/qc'])
 return len(files)
if __name__=='__main__':print('Public privacy checks complete for '+str(check())+' files')

"""Reject machine-specific paths and credential material in distributed text."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
patterns=[r'\b[A-Za-z]:[\\/]',r'/(?:home|Users|mnt|private|tmp)/',r'gh[pousr]_[A-Za-z0-9]{20,}',r'github_pat_[A-Za-z0-9_]{20,}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
excluded={'check_public_paths.py'}
def check():
 matches=[]
 for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
  _,name=line.split('  ',1);p=ROOT/name
  if p.name in excluded:continue
  try:text=p.read_text(encoding='utf-8-sig')
  except UnicodeError:continue
  for pattern in patterns:
   if re.search(pattern,text):matches.append(name)
 assert not matches,'Private paths or credential material: '+repr(matches)
if __name__=='__main__':check();print('Distributed text path checks complete')

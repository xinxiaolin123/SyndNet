"""Download and verify the frozen inference archive without credentials."""
from pathlib import Path
import argparse,hashlib,json,urllib.request,zipfile
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,default=ROOT/'downloaded_weights');a=p.parse_args()
    record=json.loads((ROOT/'weights/WEIGHT_ARCHIVE.json').read_text())
    a.output_dir.mkdir(parents=True,exist_ok=True);archive=a.output_dir/record['filename']
    if not archive.exists():
        with urllib.request.urlopen(record['url']) as source,archive.open('wb') as dest:
            for block in iter(lambda:source.read(8*1024*1024),b''):dest.write(block)
    h=hashlib.sha256()
    with archive.open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
    if h.hexdigest()!=record['sha256']:raise ValueError('Archive SHA256 mismatch; remove the incomplete file and retry')
    with zipfile.ZipFile(archive) as z:
        for name in z.namelist():
            target=(a.output_dir/name).resolve()
            if not target.is_relative_to(a.output_dir.resolve()):raise ValueError('Unsafe archive path')
        if z.testzip() is not None:raise ValueError('Archive CRC failure')
        z.extractall(a.output_dir)
    print('Verified weights extracted to '+str(a.output_dir/'weights'))
if __name__=='__main__':main()

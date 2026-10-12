"""Download and verify the frozen inference archive without credentials."""
from pathlib import Path
import argparse,hashlib,json,urllib.request,zipfile,shutil
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,default=ROOT/'downloaded_weights');p.add_argument('--archive',type=Path,help='Existing verified archive for offline extraction');a=p.parse_args()
    record=json.loads((ROOT/'weights/WEIGHT_ARCHIVE.json').read_text())
    a.output_dir.mkdir(parents=True,exist_ok=True);archive=a.archive or a.output_dir/record['filename']
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
        manifest=json.loads((ROOT/'weights/MANIFEST.json').read_text())
        # Extract only the final tensor files; distribution metadata comes from this source revision.
        for entry in manifest['files']:
            z.extract('weights/'+entry['file'],a.output_dir)
        for source in (ROOT/'weights').rglob('*'):
            if source.is_file():
                target=a.output_dir/'weights'/source.relative_to(ROOT/'weights')
                target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    print('Verified weights extracted to '+str(a.output_dir/'weights'))
if __name__=='__main__':main()

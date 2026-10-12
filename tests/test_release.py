import importlib.util,unittest,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
spec=importlib.util.spec_from_file_location('release_validator',ROOT/'scripts/validate_release.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class ReleaseIntegrity(unittest.TestCase):
 def test_distributed_integrity(self):self.assertGreater(module.validate(),80)
 def test_unmodified_apache_license(self):
  self.assertEqual(hashlib.sha256((ROOT/'LICENSE').read_bytes()).hexdigest(),'cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30')
if __name__=='__main__':unittest.main()

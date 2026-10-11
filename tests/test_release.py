import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('release_validator',ROOT/'scripts/validate_release.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class ReleaseIntegrity(unittest.TestCase):
 def test_frozen_scientific_payload(self):self.assertGreater(module.validate(),100)
 def test_unmodified_apache_license(self):
  import hashlib,json
  expected=json.loads((ROOT/'third_party/license_provenance.json').read_text())['project_license_sha256']
  self.assertEqual(hashlib.sha256((ROOT/'LICENSE').read_bytes()).hexdigest(),expected)
if __name__=='__main__':unittest.main()

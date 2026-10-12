"""Validate explicitly artificial public examples without controlled study data."""
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]
def rows(name):
 with (ROOT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def validate_formats():
 metric=rows('data/synthetic_examples/metric_predictions.csv')
 assert len(metric)==4 and all(r['example_id'].startswith('EXAMPLE_') for r in metric)
 assert all(int(r['reference_label']) in (0,1) and 0<=float(r['predicted_probability'])<=1 for r in metric)
 manifest=rows('data/example_manifest.csv')
 assert all(r['is_synthetic']=='true' and r['example_id'].startswith('EXAMPLE_') for r in manifest)
 paired=rows('reader_study_reproducibility/examples/paired_reader_format.csv')
 assignment=rows('reader_study_reproducibility/examples/reader_assignment_format.csv')
 assert all(r['reader_id'].startswith('EXAMPLE_READER_') and r['case_id'].startswith('EXAMPLE_CASE_') for r in paired)
 assert len({(r['reader_id'],r['case_id']) for r in paired})==len(paired)
 assert {r['reader_id'] for r in paired}=={r['reader_id'] for r in assignment}
 assert all(r['sequence'] in ('AB','BA') for r in assignment)
 return True
if __name__=='__main__':validate_formats();print('Artificial public formats verified; no study-statistic claim')

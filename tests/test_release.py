import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('guard', ROOT / 'scripts/check_public_release.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class ReleaseGuardTests(unittest.TestCase):
    def test_rejects_restricted_directory(self):
        self.assertTrue(guard.inspect('data/table.json', b'{}'))

    def test_rejects_clip_predictions(self):
        self.assertTrue(guard.inspect('results/predictions.csv', b'video_id,label,score_lie\n'))

    def test_rejects_sample_id_inside_text(self):
        synthetic_id = '_'.join(['ZZ', 'WILTY', 'EP0', 'lie0'])
        self.assertTrue(guard.inspect('README.md', synthetic_id.encode()))

    def test_accepts_aggregate_schema(self):
        header = ','.join(sorted(guard.CSV_FIELDS)) + '\n'
        self.assertFalse(guard.inspect('results/fold_seed_metrics.csv', header.encode()))

    def test_rejects_media(self):
        self.assertTrue(guard.inspect('sample.wav', b'RIFF'))


if __name__ == '__main__':
    unittest.main()

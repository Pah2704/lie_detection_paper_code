import ast
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


class ArchivedConfigDocumentationTests(unittest.TestCase):
    def setUp(self):
        self.tree = ast.parse((ROOT / 'src/train_multimodal.py').read_text())

    def test_legacy_training_keys_are_not_consumed(self):
        strings = {node.value for node in ast.walk(self.tree)
                   if isinstance(node, ast.Constant) and isinstance(node.value, str)}
        for key in ['lr_unfrozen_backbone', 'scheduler', 'warmup_epochs']:
            self.assertNotIn(key, strings)

    def test_executable_optimizer_and_scheduler(self):
        calls = [node for node in ast.walk(self.tree) if isinstance(node, ast.Call)
                 and isinstance(node.func, ast.Attribute)]
        optimizers = [node for node in calls if node.func.attr == 'AdamW']
        self.assertEqual(len(optimizers), 1)
        learning_rate = next(k.value for k in optimizers[0].keywords if k.arg == 'lr')
        self.assertIn('lr_head', {n.value for n in ast.walk(learning_rate)
                                  if isinstance(n, ast.Constant)})
        schedulers = [node for node in calls if node.func.attr == 'CosineAnnealingWarmRestarts']
        self.assertEqual(len(schedulers), 1)
        period = next(k.value for k in schedulers[0].keywords if k.arg == 'T_0')
        self.assertEqual(ast.literal_eval(period), 10)


if __name__ == '__main__':
    unittest.main()

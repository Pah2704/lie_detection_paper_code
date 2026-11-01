import csv
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS = ('auc_roc', 'balanced_accuracy', 'f1_lie', 'macro_f1')


def main():
    rows = list(csv.DictReader((ROOT / 'results/fold_seed_metrics.csv').open()))
    assert len(rows) == 45
    assert len({(r['method'], r['fold'], r['seed']) for r in rows}) == 45
    grouped = defaultdict(list)
    for row in rows:
        grouped[row['method']].append(row)
        if row['method'] == 'paper_gated_prior_kl' and row['seed'] == '42':
            grouped['prior_kl_seed42'].append(row)
    expected = json.loads((ROOT / 'results/aggregate_metrics.json').read_text())
    assert set(grouped) == set(expected)
    for method, records in grouped.items():
        assert len(records) == expected[method]['runs']
        for metric in METRICS:
            values = [100 * float(r[metric]) for r in records]
            for key, value in [('mean', statistics.mean(values)),
                               ('sd', statistics.stdev(values))]:
                assert math.isclose(value, expected[method][metric][key], abs_tol=1e-10)
    print('PASS: 45 run aggregates match all reported percentage means and sample SD.')


if __name__ == '__main__':
    main()

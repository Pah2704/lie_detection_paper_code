# Aggregate Results

`fold_seed_metrics.csv` contains 45 run-level records, not clip-level data:

- Three main gate conditions, three splits and three seeds: 27 runs.
- Static, flow and audio diagnostics, three splits and seed 42: 9 runs.
- Exploratory vote-score-sum, three splits and three seeds: 9 runs.

`auc_roc` uses the model scores. `balanced_accuracy`, `f1_lie` and `macro_f1`
use the threshold selected on the corresponding validation split. No fitted
probability calibration is implied. All scores in the CSV are fractions.
`threshold` is the selected run-level threshold, while `n`, `truth` and `lie`
are aggregate test counts. There is no clip ID, source URL, source timestamp or
sample-level ground-truth column.

`aggregate_metrics.json` reports percentage means and sample SD (`ddof=1`).
`prior_kl_seed42` is a three-run subset of the main Prior-KL condition, included
for the matched single-stream diagnostic; it does not add three new runs.
The exploratory vote-score-sum result is not a confirmatory main benchmark.

The released mean/SD can be regenerated from the 45 aggregate records. Computing
the original AUC from individual predictions requires authorized private inputs
and is intentionally outside the public package.


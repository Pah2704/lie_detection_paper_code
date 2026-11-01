# Controlled Gated Fusion on DOLOS

Code and aggregate experimental results for *Controlled Evaluation of Gated
Multimodal Fusion for Lie Detection Using Facial Motion and Speech Cues*.

The main comparison separates uniform initialization, directed initialization
without KL, and directed initialization with Prior-KL. Each condition uses three
predefined DOLOS splits and seeds 42, 123 and 2025. Single-stream diagnostics use
the same three splits with seed 42. Vote-score-sum is exploratory, not the main
benchmark method. The split-seed runs reuse data; their standard deviation is
descriptive and is not an independent-sample confidence interval.

## Release contents

- `src/`: preprocessing, models, training and evaluation.
- `configs/`: original experiment configurations.
- `scripts/`: original utilities, a manuscript-run wrapper and release checks.
- `results/`: fold-seed aggregate metrics and their mean/sample standard deviation.
- `SOURCE_PROVENANCE.json`: source-file checksums and the experiment source commit.

No DOLOS annotations, timestamp tables, split membership, media, caches,
checkpoints, or clip/window prediction tables are distributed. Obtain DOLOS
directly from [ROSE Lab](https://rose1.ntu.edu.sg/dataset/DOLOS/). See
[DATA_ACCESS.md](DATA_ACCESS.md) before preparing local inputs.

## Environment

The author confirmed Python 3.10.20 and NVIDIA GeForce RTX 3060 12GB as the
experimental environment. Project package versions are recorded in
[ENVIRONMENT.md](ENVIRONMENT.md). Install into a separate Python 3.10 environment:

```bash
python -m pip install -r requirements-torch-cu121.txt
python -m pip install -r requirements.txt
```

FFmpeg and FFprobe are also required for local media preparation. Their historical
versions and the GPU driver version are not recorded. Optional W&B logging is
disabled by the manuscript wrapper. No claim of a clean-environment training
reproduction is made by this code release.

## Local data preparation

Only after obtaining the provider's approval, place the authorized timestamp
table and official `Training_Protocols` directory under `data/DOLOS/`, and the
locally obtained videos under `data/raw/dolos/videos/`. These directories are
ignored by Git. The following commands write restricted local outputs:

```bash
python -m src.data.dolos_prepare --duration-audit --seed 42 --val-fraction 0.15
python -m src.data.extract_audio --metadata data/processed/splits/dolos/metadata.csv
python -m src.data.preprocess_faces_mediapipe --metadata data/processed/splits/dolos/metadata.csv
python -m src.data.extract_optical_flow --manifest data/processed/faces_224_clean/dolos/preprocess_manifest.csv --out-root data/processed/optflow_clean --method farneback
python -m src.data.filter_splits_by_cache
```

These commands create a new local dataset preparation. Current video availability
may differ from the original run. A historical clean-cache entry records
Farneback, but the backend for every historical cache was not pinned; the example
above explicitly selects Farneback and is not a claim that all original caches
used that backend. Keep every resulting annotation, membership table and
sample-level output private.

## Training and evaluation

Preview the 45 manuscript fold-seed commands without starting training:

```bash
bash scripts/run_manuscript_experiments.sh --dry-run
```

Once the authorized local inputs and caches are ready, run:

```bash
bash scripts/run_manuscript_experiments.sh
```

The new wrapper uses the active `python`; set `PYTHON_BIN` to select another
interpreter. Original archived wrappers are retained unchanged and also accept
`PYTHON_BIN` to override their original machine path.

The executable trainer uses one AdamW parameter group and
`CosineAnnealingWarmRestarts(T_0=10)`. Checkpoints are selected by validation AUC.
The decision threshold is selected on validation balanced accuracy with a
macro-F1 tie-break. This is threshold selection, not fitted probability
calibration. Original config names are retained for source traceability.

## Archived config fields and executed settings

The YAML files are the archived experiment inputs. Three legacy fields do not
control the executable trainer in `src/train_multimodal.py`:

| Archived field | Executed behavior |
| --- | --- |
| `training.lr_unfrozen_backbone: 0.00001` | Unused. All trainable parameters share one AdamW group at `training.lr_head`, which is 0.001 in the main paper configurations. Frozen backbones are excluded from optimization. |
| `training.scheduler: cosine_warmup` | Unused label. The trainer constructs `CosineAnnealingWarmRestarts(optimizer, T_0=10)` directly. |
| `training.warmup_epochs: 3` | Unused. The trainer does not implement a separate three-epoch warmup phase. |

The original YAML files are deliberately unchanged so the experiment inputs
remain traceable. Editing these unused fields does not alter training behavior.
The manuscript describes the executable optimizer and scheduler. The regression
checks in `tests/test_release.py` verify this code/config distinction; this
documentation update changes neither the model implementation nor stored results.

## Aggregate result checks

```bash
python scripts/verify_aggregate_results.py
python scripts/check_public_release.py
python -m unittest discover -s tests
```

The first command checks the released fold-seed aggregates against the reported
group means and sample SD, without reading or distributing clip-level labels.
It does not recompute AUC from predictions. Before this release, the 45 aggregate
records were independently checked against private stored predictions without
new model inference. Units and comparison scope are documented in
[results/README.md](results/README.md).

## Dataset citation

X. Guo, N. M. Selvaraj, Z. Yu, A. Kong, B. Shen, and A. Kot,
"Audio-Visual Deception Detection: DOLOS Dataset and Parameter-Efficient
Crossmodal Learning," ICCV, 2023.

The original provider's access conditions govern DOLOS. This repository does not
grant permission to redistribute the dataset or its annotations.


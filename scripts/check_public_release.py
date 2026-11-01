import csv
import io
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_FIELDS = {'method', 'fold', 'seed', 'threshold', 'auc_roc',
              'balanced_accuracy', 'f1_lie', 'macro_f1', 'n', 'truth', 'lie'}
CLIP_ID = re.compile(r'\b[A-Z]{1,5}_WILTY_EP\d+_(?:lie|truth)\d+\b', re.I)
FORBIDDEN = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.wav', '.mp3', '.jpg',
             '.jpeg', '.png', '.npz', '.npy', '.pt', '.pth', '.ckpt', '.docx',
             '.odt', '.pdf', '.zip', '.tar', '.gz', '.ipynb'}


def inspect(path, raw):
    problems = []
    p = Path(path)
    if p.parts[0] in {'data', 'outputs', 'private', 'revision'} or p.suffix.lower() in FORBIDDEN:
        problems.append('restricted path or file type')
    if p.name == '.env' or p.name.startswith('.env.'):
        problems.append('environment secret file')
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        return problems + ['non-text content']
    if CLIP_ID.search(text):
        problems.append('sample-level source ID')
    if re.search(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16})\b', text):
        problems.append('possible credential')
    if p.suffix == '.csv':
        rows = list(csv.reader(io.StringIO(text)))
        if str(p) != 'results/fold_seed_metrics.csv' or not rows or set(rows[0]) != CSV_FIELDS:
            problems.append('CSV is not the approved run-aggregate schema')
    return problems


def main():
    if (ROOT / '.git').exists():
        paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
        paths = [p for p in paths if p]
    else:
        paths = [str(p.relative_to(ROOT)) for p in ROOT.rglob('*')
                 if p.is_file() and '__pycache__' not in p.parts]
    failures = {p: issues for p in paths if (issues := inspect(p, (ROOT / p).read_bytes()))}
    if failures:
        for path, issues in failures.items():
            print(f'FAIL {path}: {", ".join(issues)}')
        raise SystemExit(1)
    print(f'PASS: {len(paths)} release files contain no flagged restricted paths, media, source IDs or sample-level CSV schemas.')


if __name__ == '__main__':
    main()

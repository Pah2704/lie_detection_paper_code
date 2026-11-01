#!/usr/bin/env bash
set -euo pipefail

PYTHON_CMD="${PYTHON_BIN:-python}"
DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
elif [[ $# -ne 0 ]]; then
  printf 'Usage: bash scripts/run_manuscript_experiments.sh [--dry-run]\n' >&2
  exit 2
fi

run_train() {
  local config="$1" fold="$2" seed="$3"
  local command=("${PYTHON_CMD}" -m src.train_multimodal --config "${config}" --fold "${fold}" --seed "${seed}" --no-wandb)
  if [[ "${DRY_RUN}" == true ]]; then
    printf '%q ' "${command[@]}"
    printf '\n'
  else
    "${command[@]}"
  fi
}

for config in paper_gated_neutral_no_prior paper_gated_no_prior paper_gated_prior_kl; do
  for seed in 42 123 2025; do
    for fold in fold1 fold2 fold3; do
      run_train "configs/${config}.yaml" "${fold}" "${seed}"
    done
  done
done

for config in paper_ablation_static paper_ablation_flow paper_ablation_audio; do
  for fold in fold1 fold2 fold3; do
    run_train "configs/${config}.yaml" "${fold}" 42
  done
done

for seed in 42 123 2025; do
  for fold in fold1 fold2 fold3; do
    run_train configs/paper_gated_vote_score_sum_g05_floor005.yaml "${fold}" "${seed}"
  done
done


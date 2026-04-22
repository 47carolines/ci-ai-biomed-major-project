#!/bin/bash

# ==============================
# DeepPrep Pipeline Runner
# Submission II - CI-AI Project
# ==============================

set -e  # stop if anything fails

PROJECT_ROOT=$(pwd)

DATA_DIR="$PROJECT_ROOT/submission_ii/data/ds006628"
OUTPUT_DIR="$PROJECT_ROOT/submission_ii/outputs/deepprep_results"
LICENSE_FILE="$PROJECT_ROOT/submission_ii/license.txt"

echo "Starting DeepPrep pipeline..."
echo "Input:  $DATA_DIR"
echo "Output: $OUTPUT_DIR"

mkdir -p "$OUTPUT_DIR"

docker run --rm \
  --platform linux/amd64 \
  -v "$DATA_DIR:/input" \
  -v "$OUTPUT_DIR:/output" \
  -v "$LICENSE_FILE:/fs_license.txt" \
  pbfslab/deepprep:25.1.0 \
  /input \
  /output \
  participant \
  --participant_label sub-01 \
  --bold_task_type response feature dimension \
  --fs_license_file /fs_license.txt \
  --device cpu

echo "DeepPrep completed successfully."
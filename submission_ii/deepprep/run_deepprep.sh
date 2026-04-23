#!/bin/bash

# ==============================
# DeepPrep Pipeline Runner
# Submission II - CI-AI Project
# ==============================

set -e

# Resolve absolute path to script location (ROBUST)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

DATA_DIR="$PROJECT_ROOT/data/test_sample"
OUTPUT_DIR="$PROJECT_ROOT/outputs/deepprep_results"
LICENSE_FILE="$PROJECT_ROOT/license.txt"

echo "Starting DeepPrep pipeline..."
echo "Project root: $PROJECT_ROOT"
echo "Input:  $DATA_DIR"
echo "Output: $OUTPUT_DIR"

# ------------------------------
# VALIDATION CHECKS
# ------------------------------

if [ ! -d "$DATA_DIR/sub-01" ]; then
  echo "ERROR: sub-01 not found in dataset at $DATA_DIR"
  exit 1
fi

if [ ! -f "$LICENSE_FILE" ]; then
  echo "ERROR: FreeSurfer license not found at $LICENSE_FILE"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

# ------------------------------
# RUN DOCKER
# ------------------------------

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
  --bold_task_type 6cat \
  --fs_license_file /fs_license.txt \
  --device cpu

echo "DeepPrep completed successfully."
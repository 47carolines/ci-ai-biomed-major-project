#!/bin/bash

# ==============================
# DeepPrep Pipeline Runner
# Submission II - CI-AI Project
# ==============================

set -e

# ------------------------------
# PATH SETUP
# ------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

DATA_DIR="$PROJECT_ROOT/data/test_sample"
OUTPUT_DIR="$PROJECT_ROOT/output"
LICENSE_FILE="$PROJECT_ROOT/license/license.txt"

PARTICIPANT="sub-01"
BOLD_TASK="6cat"

echo "======================================"
echo "Starting DeepPrep pipeline"
echo "Project root : $PROJECT_ROOT"
echo "Input        : $DATA_DIR"
echo "Output       : $OUTPUT_DIR"
echo "Participant  : $PARTICIPANT"
echo "Task         : $BOLD_TASK"
echo "======================================"

# ------------------------------
# VALIDATION CHECKS
# ------------------------------

if [ ! -d "$DATA_DIR" ]; then
  echo "ERROR: Dataset directory not found at $DATA_DIR"
  exit 1
fi

if [ ! -d "$DATA_DIR/$PARTICIPANT" ]; then
  echo "ERROR: $PARTICIPANT not found in dataset"
  exit 1
fi

if [ ! -f "$DATA_DIR/dataset_description.json" ]; then
  echo "ERROR: Missing dataset_description.json (invalid BIDS dataset)"
  exit 1
fi

if [ ! -f "$LICENSE_FILE" ]; then
  echo "ERROR: FreeSurfer license not found at $LICENSE_FILE"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

# ------------------------------
# GPU AUTO-DETECTION (optional)
# ------------------------------

if command -v nvidia-smi &> /dev/null; then
  echo "GPU detected → attempting GPU mode"
  DEVICE_FLAG="auto"
  GPU_FLAG="--gpus all"
else
  echo "No GPU detected → using CPU mode"
  DEVICE_FLAG="cpu"
  GPU_FLAG=""
fi

# ------------------------------
# RUN DEEPPREP
# ------------------------------

docker run --rm \
  $GPU_FLAG \
  -v "$DATA_DIR:/input" \
  -v "$OUTPUT_DIR:/output" \
  -v "$LICENSE_FILE:/fs_license.txt" \
  pbfslab/deepprep:25.1.0 \
  /input \
  /output \
  participant \
  --participant_label "$PARTICIPANT" \
  --bold_task_type "$BOLD_TASK" \
  --fs_license_file /fs_license.txt \
  --device "$DEVICE_FLAG" \
  --cpus 8 \
  --memory 28

echo "======================================"
echo "DeepPrep completed successfully"
echo "Output saved to: $OUTPUT_DIR"
echo "======================================"
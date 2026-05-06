#!/bin/bash

# ==============================
# DeepPrep Pipeline Runner
# Submission II - CI-AI Project (UPDATED FOR ds005237 + SCALE)
# ==============================

set -e

# ------------------------------
# INPUT ARGUMENT (IMPORTANT FOR 10-NODE SCALE)
# ------------------------------
if [ -z "$1" ]; then
  echo "ERROR: Please provide a participant ID (e.g., sub-NDARINVXXXX)"
  exit 1
fi

PARTICIPANT="$1"

# ------------------------------
# PATH SETUP
# ------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

DATA_DIR="$PROJECT_ROOT/data/ds005237"
OUTPUT_DIR="$PROJECT_ROOT/output/$PARTICIPANT"
LICENSE_FILE="$PROJECT_ROOT/license/license.txt"

echo "======================================"
echo "Starting DeepPrep pipeline"
echo "Project root : $PROJECT_ROOT"
echo "Input        : $DATA_DIR"
echo "Output       : $OUTPUT_DIR"
echo "Participant  : $PARTICIPANT"
echo "======================================"

# ------------------------------
# VALIDATION CHECKS
# ------------------------------

if [ ! -d "$DATA_DIR" ]; then
  echo "ERROR: Dataset directory not found at $DATA_DIR"
  exit 1
fi

if [ ! -d "$DATA_DIR/$PARTICIPANT" ]; then
  echo "ERROR: Participant not found: $PARTICIPANT"
  exit 1
fi

if [ ! -f "$LICENSE_FILE" ]; then
  echo "ERROR: FreeSurfer license not found at $LICENSE_FILE"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

# ------------------------------
# RESOURCE SETTINGS (FABRIC SAFE)
# ------------------------------

DEVICE_FLAG="cpu"
CPUS=6
MEMORY=22

echo "Using CPU mode"
echo "CPUs   : $CPUS"
echo "Memory : $MEMORY GB"

# ------------------------------
# RUN DEEPPREP
# ------------------------------

docker run --rm \
  -v "$DATA_DIR:/input" \
  -v "$OUTPUT_DIR:/output" \
  -v "$LICENSE_FILE:/fs_license.txt" \
  pbfslab/deepprep:25.1.0 \
  /input \
  /output \
  participant \
  --participant_label "$PARTICIPANT" \
  --fs_license_file /fs_license.txt \
  --device "$DEVICE_FLAG" \
  --cpus "$CPUS" \
  --memory "$MEMORY" \
  --bold_task_type rest \
  --bold_sdc \
  --bold_confounds \
  --bold_volume_space MNI152NLin2009cAsym \
  --bold_volume_res 02 \
  --bold_surface_spaces 'fsaverage6'

echo "======================================"
echo "DeepPrep completed successfully"
echo "Output saved to: $OUTPUT_DIR"
echo "======================================"
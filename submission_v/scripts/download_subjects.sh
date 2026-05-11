#!/bin/bash

# ==========================
# OpenNeuro Subject Download
# ds005237 (TEAM TEMPLATE)
# ==========================

BASE_DIR=~/deepprep_project/data/ds005237

# --------------------------
# EDIT THIS PER TEAM MEMBER
# --------------------------

# Caroline:
# sub-NDARINVAG023WG3
# sub-NDARINVAG339WHH
# sub-NDARINVZX212UNE

# Noor:
# sub-NDARINVUR466KN5
# sub-NDARINVJP343BJ6
# sub-NDARINVFH503ZWA

# Scott:
# sub-NDARINVKX727WL8
# sub-NDARINVUY799LKJ
# sub-NDARINVWD338PY2

SUBJECTS=(
sub-NDARINVAG023WG3
sub-NDARINVAG339WHH
sub-NDARINVXXXXXXX # placeholder subjects, edit before running
)

mkdir -p "$BASE_DIR"

# --------------------------
# 1. DOWNLOAD SUBJECTS
# --------------------------

for sub in "${SUBJECTS[@]}"; do
  echo "Downloading $sub ..."
  aws s3 cp --no-sign-request --recursive \
    s3://openneuro.org/ds005237/$sub \
    "$BASE_DIR/$sub"
done

# --------------------------
# 2. DOWNLOAD DATASET METADATA (IMPORTANT FOR DEEPPREP)
# --------------------------

echo "Downloading dataset_description.json ..."

aws s3 cp --no-sign-request \
  s3://openneuro.org/ds005237/dataset_description.json \
  "$BASE_DIR/dataset_description.json"

# --------------------------
# 3. FINAL CHECK
# --------------------------

echo "Verifying dataset structure:"
ls "$BASE_DIR"

echo "Download complete."
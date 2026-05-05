#!/bin/bash

# --------------------------
# EDIT THIS PER TEAM MEMBER
# --------------------------

# Caroline:
# - sub-NDARINVAG023WG3
# - sub-NDARINVAG339WHH
# - sub-NDARINVZX212UNE

# Noor:
# - sub-NDARINVUR466KN5
# - sub-NDARINVJP343BJ6
# - sub-NDARINVFH503ZWA

# Scott:
# - sub-NDARINVKX727WL8
# - sub-NDARINVUY799LKJ
# - sub-NDARINVWD338PY2


SUBJECTS=(
  sub-NDARINVAG023WG3
  sub-NDARINVAG339WHH
  sub-NDARINVXXXXXXXX
)

for SUB in "${SUBJECTS[@]}"
do
  echo "Starting $SUB..."
  ./run_deepprep.sh $SUB
  echo "Finished $SUB"
done
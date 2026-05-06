import os
import numpy as np
import pandas as pd

from scipy.stats import zscore

# ----------------------------
# CONFIG
# ----------------------------
DATA_DIR = "/home/ubuntu/deepprep_project/output"
OUTPUT_PATH = "/home/ubuntu/deepprep_project/subject_features.csv"

BOLD_COLS = [f"ts_{k}" for k in range(720)]  # adjust if needed

# ----------------------------
# FEATURE FUNCTIONS
# ----------------------------
def compute_fc_matrix(timeseries):
    """
    timeseries: shape (ROIs, timepoints)
    """
    return np.corrcoef(timeseries)


def upper_triangle(matrix):
    return matrix[np.triu_indices(matrix.shape[0], k=1)]


def load_subject_bold(subject_path):
    """
    Expected: ROI-sorted table inside DeepPrep WorkDir or exported file
    You may need to adjust filename depending on your pipeline
    """
    # Try common DeepPrep pattern (adjust if needed)
    possible_files = [
        os.path.join(subject_path, "WorkDir", "bold_table.csv"),
        os.path.join(subject_path, "bold_table.csv"),
    ]

    for f in possible_files:
        if os.path.exists(f):
            df = pd.read_csv(f)
            return df

    raise FileNotFoundError(f"No BOLD table found in {subject_path}")


def process_subject(subject_id):
    subject_path = os.path.join(DATA_DIR, subject_id)

    bold_df = load_subject_bold(subject_path)

    bold_df = bold_df.sort_values("ROI")

    fmri_matrix = bold_df[BOLD_COLS].dropna(axis=1).to_numpy()

    # Z-score per ROI
    fmri_matrix = zscore(fmri_matrix, axis=1, nan_policy='omit')

    # FC matrix
    fc = compute_fc_matrix(fmri_matrix)

    fc_vec = upper_triangle(fc)

    # Placeholder target (replace with real metadata if available)
    ftnd = bold_df["FTND"].iloc[0] if "FTND" in bold_df.columns else np.nan

    return fc_vec, ftnd


# ----------------------------
# MAIN PIPELINE
# ----------------------------
subjects = [
    d for d in os.listdir(DATA_DIR)
    if d.startswith("sub-")
]

all_features = []
targets = []

for sub in subjects:
    try:
        fc_vec, target = process_subject(sub)

        all_features.append(fc_vec)
        targets.append(target)

        print(f"Processed {sub}")

    except Exception as e:
        print(f"FAILED {sub}: {e}")


all_features = np.array(all_features)
targets = np.array(targets)

df = pd.DataFrame(all_features)
df["target"] = targets

df.to_csv(OUTPUT_PATH, index=False)

print("DONE → saved to:", OUTPUT_PATH)
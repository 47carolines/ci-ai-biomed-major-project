import os
import pandas as pd
import numpy as np

DATA_DIR = "/home/ubuntu/deepprep_project/output"
OUTPUT_PATH = "/home/ubuntu/deepprep_project/subject_features.csv"


def load_confounds(subject_dir):
    candidates = [
        f for f in os.listdir(subject_dir)
        if f.endswith("desc-confounds_timeseries.tsv")
    ]

    if not candidates:
        raise FileNotFoundError("No confounds file found")

    return pd.read_csv(os.path.join(subject_dir, candidates[0]), sep="\t")


def compute_features(df):
    features = {}

    if "framewise_displacement" in df.columns:
        fd = df["framewise_displacement"].fillna(0)
        features["fd_mean"] = fd.mean()
        features["fd_max"] = fd.max()
        features["fd_std"] = fd.std()
        features["fd_spikes"] = (fd > 0.5).sum()

    if "std_dvars" in df.columns:
        dvars = df["std_dvars"].dropna()
        features["dvars_mean"] = dvars.mean()

    return features


rows = []

for sub in os.listdir(DATA_DIR):
    if not sub.startswith("sub-"):
        continue

    try:
        confound_path = os.path.join(
            DATA_DIR,
            sub,
            "BOLD",
            sub,
            "func"
        )

        df = load_confounds(confound_path)
        feats = compute_features(df)

        feats["subject"] = sub
        rows.append(feats)

        print("Processed", sub)

    except Exception as e:
        print("FAILED", sub, e)


pd.DataFrame(rows).to_csv(OUTPUT_PATH, index=False)
print("Saved:", OUTPUT_PATH)
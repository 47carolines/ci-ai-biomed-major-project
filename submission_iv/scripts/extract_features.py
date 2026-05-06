import os
import pandas as pd
import numpy as np

DATA_DIR = "/home/ubuntu/deepprep_project/output"
OUTPUT_PATH = "/home/ubuntu/deepprep_project/subject_features.csv"


# ----------------------------
# LOAD CONFOUNDS
# ----------------------------
def load_confounds(subject_dir):
    candidates = [
        f for f in os.listdir(subject_dir)
        if f.endswith("desc-confounds_timeseries.tsv")
    ]

    if not candidates:
        raise FileNotFoundError("No confounds file found")

    return pd.read_csv(os.path.join(subject_dir, candidates[0]), sep="\t")


# ----------------------------
# LOAD BOLD TIMESERIES
# ----------------------------
def load_bold_timeseries(subject_dir):
    """
    Tries to find a usable BOLD time series table.
    Adjust if your DeepPrep output differs.
    """
    func_dir = subject_dir

    candidates = []
    for root, _, files in os.walk(func_dir):
        for f in files:
            if f.endswith(".tsv") and "confounds" not in f:
                candidates.append(os.path.join(root, f))

    if not candidates:
        raise FileNotFoundError("No BOLD timeseries file found")

    # pick first valid candidate
    return pd.read_csv(candidates[0], sep="\t")


# ----------------------------
# CONFOUNDS FEATURES
# ----------------------------
def compute_confound_features(df):
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


# ----------------------------
# BOLD FEATURES (NEW - WALTS DIRECTION)
# ----------------------------
def compute_bold_features(df):
    """
    Assumes df contains ROI time series columns OR numeric signal columns.
    """
    features = {}

    # keep only numeric columns (drop metadata)
    ts = df.select_dtypes(include=[np.number]).to_numpy()

    if ts.size == 0:
        return features

    # --------------------
    # Time-domain features
    # --------------------
    mean_signal = np.mean(ts)
    std_signal = np.std(ts)

    features["bold_mean_amp"] = mean_signal
    features["bold_std_amp"] = std_signal

    # --------------------
    # Frequency-domain features (FFT)
    # --------------------
    fft_vals = np.fft.rfft(ts, axis=1 if ts.ndim > 1 else 0)
    power = np.abs(fft_vals) ** 2

    total_power = np.sum(power)
    features["spectral_total_power"] = total_power

    # low-frequency proxy (first ~10 bins)
    if power.ndim == 2:
        features["spectral_low_freq_power"] = np.sum(power[:, :10])
    else:
        features["spectral_low_freq_power"] = np.sum(power[:10])

    return features


# ----------------------------
# MAIN LOOP
# ----------------------------
rows = []

for sub in os.listdir(DATA_DIR):
    if not sub.startswith("sub-"):
        continue

    try:
        subject_dir = os.path.join(DATA_DIR, sub)

        # confounds
        confound_path = os.path.join(subject_dir, "BOLD", sub, "func")
        confounds_df = load_confounds(confound_path)
        confound_feats = compute_confound_features(confounds_df)

        # BOLD features
        bold_df = load_bold_timeseries(confound_path)
        bold_feats = compute_bold_features(bold_df)

        # merge
        feats = {**confound_feats, **bold_feats}
        feats["subject"] = sub

        rows.append(feats)

        print("Processed", sub)

    except Exception as e:
        print("FAILED", sub, e)


# ----------------------------
# SAVE CSV
# ----------------------------
pd.DataFrame(rows).to_csv(OUTPUT_PATH, index=False)
print("Saved:", OUTPUT_PATH)
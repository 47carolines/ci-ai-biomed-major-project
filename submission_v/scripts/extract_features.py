import os
import numpy as np
import pandas as pd

from nilearn import image

DATA_DIR = "/home/ubuntu/deepprep_project/output"
OUTPUT_PATH = "/home/ubuntu/deepprep_project/subject_features.csv"


# ----------------------------
# FIND FILES
# ----------------------------
def find_confounds(func_dir):
    for f in os.listdir(func_dir):
        if f.endswith("desc-confounds_timeseries.tsv"):
            return os.path.join(func_dir, f)
    return None


def find_bold(func_dir):
    for f in os.listdir(func_dir):
        if "desc-preproc_bold.nii.gz" in f:
            return os.path.join(func_dir, f)
    return None


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
# BOLD FEATURES (REAL SIGNAL)
# ----------------------------
def compute_bold_features(bold_img_path):
    features = {}

    img = image.load_img(bold_img_path)
    data = img.get_fdata()

    # data shape: (x, y, z, time)
    if len(data.shape) != 4:
        return features

    # -----------------------
    # Flatten brain voxels → time series
    # -----------------------
    ts = data.reshape(-1, data.shape[-1])  # voxels × time

    # remove empty voxels
    ts = ts[np.std(ts, axis=1) > 0]

    if ts.shape[0] == 0:
        return features

    # -----------------------
    # Time-domain features
    # -----------------------
    voxel_mean = np.mean(ts)
    voxel_std = np.std(ts)

    features["bold_mean_signal"] = voxel_mean
    features["bold_std_signal"] = voxel_std

    # variance across time per voxel
    voxel_var = np.var(ts, axis=1)
    features["bold_mean_voxel_variance"] = np.mean(voxel_var)

    # -----------------------
    # Temporal signal (global mean signal)
    # -----------------------
    global_ts = np.mean(ts, axis=0)

    features["bold_global_mean"] = np.mean(global_ts)
    features["bold_global_std"] = np.std(global_ts)

    # -----------------------
    # Spectral features (FFT)
    # -----------------------
    fft_vals = np.fft.rfft(global_ts)
    power = np.abs(fft_vals) ** 2

    features["spectral_total_power"] = np.sum(power)
    features["spectral_low_freq_power"] = np.sum(power[:10])

    return features


# ----------------------------
# MAIN PIPELINE
# ----------------------------
rows = []

for sub in os.listdir(DATA_DIR):
    if not sub.startswith("sub-"):
        continue

    try:
        subject_dir = os.path.join(DATA_DIR, sub, "BOLD", sub, "func")

        # -----------------------
        # confounds
        # -----------------------
        conf_path = find_confounds(subject_dir)
        if conf_path is None:
            raise FileNotFoundError("confounds missing")

        conf_df = pd.read_csv(conf_path, sep="\t")
        conf_feats = compute_confound_features(conf_df)

        # -----------------------
        # BOLD
        # -----------------------
        bold_path = find_bold(subject_dir)
        if bold_path is None:
            raise FileNotFoundError("BOLD NIfTI missing")

        bold_feats = compute_bold_features(bold_path)

        # -----------------------
        # merge
        # -----------------------
        feats = {**conf_feats, **bold_feats}
        feats["subject"] = sub

        rows.append(feats)

        print("Processed", sub)

    except Exception as e:
        print("FAILED", sub, e)


# ----------------------------
# SAVE
# ----------------------------
pd.DataFrame(rows).to_csv(OUTPUT_PATH, index=False)
print("Saved:", OUTPUT_PATH)
# Submission II – DeepPrep fMRI Preprocessing Pipeline

## 📌 Prerequisites / Assumptions

This README assumes the user is already operating inside the `submission_ii/` directory.

All relative paths in commands (e.g., `cd deepprep`, `./run_deepprep.sh`) are based on this working directory.

The following files and folders are expected to exist:

- `deepprep/` (contains `run_deepprep.sh`)
- `data/` (BIDS-formatted dataset)
- `outputs/` (auto-generated during execution)
- `license.txt` (FreeSurfer license file)
## ⚙️ Execution / Reproducibility

To run the DeepPrep preprocessing pipeline, navigate into the DeepPrep directory and execute the provided script:

```bash
cd deepprep
bash run_deepprep.sh
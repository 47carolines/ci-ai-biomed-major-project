# CI-AI Biomedical Engineering Major Project  
## DeepPrep fMRI Preprocessing and Spectral Feature Analysis

---

## 📌 Project Overview

This project implements a reproducible end-to-end functional MRI (fMRI) preprocessing and analysis pipeline using the DeepPrep framework on FABRIC infrastructure. The goal is to extract high-dimensional spectral and temporal features from BOLD signals and establish a healthy control baseline for future neurobiological comparison studies (e.g., nicotine dependence).

The pipeline processes subject-level data from [OpenNeuro (ds005237)](https://openneuro.org/datasets/ds005237/versions/1.1.3), performs preprocessing using Dockerized DeepPrep, and extracts motion, functional, and spectral features for downstream statistical analysis.

---

## 📁 Repository Structure
### Submission_II
* Initial setup scripts and early pipeline exploration

### Submission_IV
* Full DeepPrep pipeline implementation
* FABRIC VM setup
* Docker workflow
* Subject-level preprocessing scripts
* Feature extraction pipeline

### Submission_V
* Final analysis and results
* Feature correlation analysis
* Statistical summaries
* Presentation materials and demo preparation

---

## ⚙️ Pipeline Summary

1. FABRIC VM provisioning and environment setup  
2. Docker installation and DeepPrep container execution  
3. Subject-level preprocessing (OpenNeuro ds005237 subset)  
4. Motion correction, normalization, and QC generation  
5. Feature extraction (FD, DVARS, ALFF, spectral power, connectivity)  
6. CSV aggregation for statistical analysis  
7. Final correlation and spectral analysis

---

## 📊 Key Outputs

- Preprocessed fMRI data (DeepPrep derivatives)
- Quality control reports (HTML)
- Subject-level feature matrices (CSV)
- Correlation matrices and statistical visualizations
- Final combined dataset for analysis

---

## 🎥 Final Demo

A complete walkthrough of the pipeline, including VM execution, preprocessing, and analysis, is available below:

▶️ YouTube Demo (Unlisted): https://youtu.be/nuVT9tjOurw?si=QB9XyyWGgDfG6hY0

The demo includes:
- FABRIC VM setup and execution
- Running DeepPrep on selected subjects
- Feature extraction pipeline
- Final analysis and visualization results

---

## 👥 Team Contributions

- **Scott** – Power analysis and sample size estimation, statistical support, ran ~3 subjects through pipeline, co-authored final report  
- **Caroline** – Pipeline design and integration, DeepPrep workflow implementation, mock presentation design, demo recording, final submission coordination, ran ~3 subjects through pipeline  
- **Noor** – Data handling and execution support, ran ~3 subjects through pipeline, contributed to final report and analysis integration  

Each member contributed to subject-level processing, enabling distributed execution of the pipeline and ensuring reproducibility across the dataset.

---

## 📌 Notes

- The project follows a reproducible, containerized workflow using Docker and FABRIC infrastructure.
- Each subject is processed independently to allow scalable parallel execution.
- Final results are based on aggregated subject-level feature extraction.

---

## 🧠 Key Technologies

- DeepPrep (fMRI preprocessing)
- FABRIC testbed infrastructure
- Docker
- Python (NumPy, Pandas, Nilearn, SciPy)
- OpenNeuro dataset (ds005237)
- Neuroimaging feature extraction and spectral analysis

---
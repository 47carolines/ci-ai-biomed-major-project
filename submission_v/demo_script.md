# 🎥 DeepPrep Final Demo Script (FABRIC Pipeline)

1. SSH into FABRIC Node
```
ssh -F ~/.ssh/config.txt -i ~/.ssh/fabric-sliver-key ubuntu@2001:1948:417:7:f816:3eff:fe41:31e3
```

2. Navigate to project
```
cd ~/deepprep_project
ls
```

3. Show pipeline structure

Point out directory organization:

* data/ → BIDS input subjects
* output/ → DeepPrep derivatives
* scripts/ → automation + reproducibility
* license/ → FreeSurfer license

4. Show processed outputs
```
cd output
ls
```
Point out:

* subject folders
* QC folder

5. Open QC report

Navigate:
```
cd qc_reports
ls
```
Open locally:

* report_AG023WG3.html
* report_AG339WHH.html
* report_ZX212UNE.html

6.  Show feature extraction output
```
cd ~/deepprep_project
head caroline_subject_features.csv
```
# Submission II – DeepPrep fMRI Preprocessing Pipeline

# Getting setup:
## Part 1: Creating and SSHing into FABRIC VM

Disclaimer: This documentation assumes you have a FABRIC account, you are in the CI4Neuroscience Project, and you have set up a sliver and bastion keys for your account and that you have them locally on your computer. If not, please watch and follow along Ajay's FABRIC setup video from Week 3 on Canvas.

1. Go to FABRIC Portal website here: https://portal.fabric-testbed.net/ and Log in using your umsystem credentials.
2. Click on Experiments in the top navbar and then click Projects & Slices, then click CI4Neuroscience. Then click Slices, and click the Create Slice button.
3. Enter the following node information:

Step 2: Add Nodes Section
* Site: UTAH
* Node Name: major-sub-ii
* Cores: 8
* RAM (GB): 32
* Disk (GB): 100
* OS Image: Ubuntu 20

---
### GPU Support (Optional)

DeepPrep supports GPU acceleration for certain deep-learning components
(e.g., segmentation and morphing models). If a CUDA-enabled GPU is available
and properly configured on the system, users may enable GPU execution using:

--gpus all --device auto

However, CPU-only execution is fully supported and is the default configuration
used in this setup to ensure compatibility across FABRIC VM environments.

In that case you would add:
* Component Type: GPU
* Name: sub-ii-gpu
* Model: A40
---

Step 4: Create Slice Section
* Slice Name: test_slice
* SSH Keys: fabric-sliver-key

Click Create Slice when you are ready. Wait up to 2-3 minutes for the slice to provision.

Once the slice status is Green or StableOk, click the white square which is your node in your topology. Then you should be able to see the SSH Command. Click the copy icon on the SSH Command it and go to a terminal on your computer. It should look something like this, but with your unique hostname:
```
ssh -F <path to SSH config file> -i <path to private sliver key> ubuntu@2001:1948:417:7:f816:3eff:fe92:eb83
```
![alt text](<assets/stable-slice.png>)

Navigate to the folder you have your config and private sliver key in. Enter the SSH command and you should be inside the node.
![alt text](assets/ssh-success.png)

# Part 2: Installing DeepPrep and Setting up on VM
These instructions are adapted from DeepPrep documentation: https://deepprep.readthedocs.io/en/latest/index.html

## 2.1: Installing Docker on the VM

After successfully SSHing into the FABRIC VM, the next step is to install Docker, which is required to run DeepPrep.


### 2.1.1 Update system packages

```
sudo apt update
sudo apt upgrade -y
```

### 2.1.2 Install Docker (recommended method for FABRIC VM)

Since the VM is Ubuntu 20.04, Docker can be installed directly from the Ubuntu package manager:
`sudo apt install -y docker.io`

### 2.1.3 Start and enable Docker service
```
sudo systemctl start docker
sudo systemctl enable docker
```

### 2.1.4 Verify Docker installation

Run the following command to confirm Docker is working correctly:
`docker run hello-world`


### 2.1.5 Fixing Docker Permission Denied Error

After installing Docker, you may encounter the following error when running a Docker command:

`permission denied while trying to connect to the Docker daemon socket`

This occurs because the current user does not have permission to access the Docker daemon.

### Temporary fix (recommended for immediate use)

Use sudo to run Docker commands:

`sudo docker run hello-world`

This allows Docker to run without changing system permissions.

### Permanent fix (recommended setup)

To allow Docker to run without sudo, add your user to the Docker group:

`sudo usermod -aG docker $USER`

Apply the group changes immediately:

`newgrp docker`

Then verify Docker works without sudo:

`docker run hello-world`

## 2.2 Pulling and Testing the DeepPrep Docker Image

After Docker has been installed and verified on the VM, the next step is to download and test the DeepPrep container.

---

### 2.2.1 Pull the DeepPrep Docker image

Run the following command to download the DeepPrep image from DockerHub:

`docker pull pbfslab/deepprep:25.1.0`

### 2.2.2 Run the Docker image (test execution)
To verify that the container is functioning correctly, run:
`docker run --rm pbfslab/deepprep:25.1.0`

### 2.2.3 Expected output

If the image was successfully pulled and executed, the terminal should display usage information similar to the following:
```
INFO: args:
DeepPrep args:
deepprep-docker [bids_dir] [output_dir] [{participant}] [--bold_task_type '[task1 task2 task3 ...]']
                [--fs_license_file PATH] [--participant_label '[001 002 003 ...]']
                [--subjects_dir PATH] [--skip_bids_validation]
                [--anat_only] [--bold_only] [--bold_sdc] [--bold_confounds] [--bold_skip_frame 0]
                [--bold_cifti] [--bold_surface_spaces '[None fsnative fsaverage fsaverage6 ...]']
                [--bold_volume_space {None MNI152NLin6Asym MNI152NLin2009cAsym}]
                [--bold_volume_res {02 03...}]
                [--device {auto 0 1 2... cpu}]
                [--cpus 10] [--memory 20]
                [--ignore_error] [--resume]
```                
## 2.3 Running DeepPrep on the FABRIC VM

Once Docker is installed (Section 2.1) and the DeepPrep image has been successfully pulled and verified (Section 2.2), you are ready to run the preprocessing pipeline on the VM.

This project uses a wrapper script (run_deepprep.sh) to simplify execution of the DeepPrep Docker container on FABRIC.

### 🏃‍♀️ 2.3.1 Quick Start (test dataset)
Get started with a test_sample, using curl to download test sample file.

```
curl -C - -O https://download.anning.info/ninganme-public/DeepPrep/TestDataset/test_sample.zip
```
### 📦 Unzip the dataset
```
sudo apt install unzip
unzip test_sample.zip
```
This will create a BIDS-formatted directory containing:

* 1 subject
* 1 anatomical image
* 2 functional (BOLD) runs

### 📁 Example structure
```
test_sample/
├── sub-01/
│   ├── anat/
│   └── func/
└── dataset_description.json
```

## 2.3.2 Requirements (license + assumptions)

### 🔑 FreeSurfer License Setup

DeepPrep requires a valid FreeSurfer license to run preprocessing steps.

If you do not already have one, you can obtain it for free by registering here:

👉 https://surfer.nmr.mgh.harvard.edu/registration.html


### 📁 Place the license on the VM

After downloading, copy your license file into the project directory:

```
mkdir -p ~/deepprep_project/license
cp ~/freesurfer/license.txt ~/deepprep_project/license/
```

Your file should now be located at:

```~/deepprep_project/license/license.txt```


### 🧠 Why this is required

DeepPrep uses FreeSurfer internally for:

* anatomical reconstruction
* surface registration
* segmentation steps

Without a valid license, the pipeline will fail during preprocessing.


### 📌 How it is used in Docker

The license is mounted into the container:

`-v $FS_LICENSE:/fs_license.txt`

Inside the container, DeepPrep expects:

`/fs_license.txt`


### ⚠️ Important note (this is where students usually mess up)

Make sure:

* the file is named exactly license.txt
* it is not empty
* it is readable:

`chmod 644 ~/deepprep_project/license/license.txt`


## 2.3.3 📁 VM Folder Setup

After downloading the test dataset, organize your workspace on the VM as follows. You will have to copy `license.txt` and `run_deepprep.sh` from your local machine.
```
~/deepprep_project/
├── data/
│   ├── test_sample/
├── output/
├── license/
│   └── license.txt
├── scripts/
│   └── run_deepprep.sh
```

Here are some example ways to do that:
```
mkdir -p ~/deepprep_project/data/test_sample
mv ~/sub-01 ~/deepprep_project/data/test_sample/
mv ~/dataset_description.json ~/deepprep_project/data/test_sample/
mv ~/README ~/deepprep_project/data/test_sample/
```

Verify setup with tree:
```
sudo apt install tree
tree ~/deepprep_project/
```

## ▶️ 2.3.5 Running DeepPrep

Make sure your script is executable:
```
chmod +x ~/deepprep_project/scripts/run_deepprep.sh
```

Run the pipeline:
```
cd ~/deepprep_project/scripts
./run_deepprep.sh
```

## ⚙️ 2.3.6 What the Script Does

The run_deepprep.sh script:

* Validates dataset structure (BIDS format)
* Checks FreeSurfer license
* Mounts input/output directories into Docker
* Runs DeepPrep preprocessing pipeline
* Processes subject sub-01 using task 6cat
* Outputs results to:
  
```
~/deepprep_project/output/
```

## 📌 2.3.7 Expected Output

If successful, DeepPrep will generate:

* Preprocessed anatomical outputs
* Preprocessed BOLD fMRI outputs
* QC reports and derivatives

Output will be stored in:
```
~/deepprep_project/output/
```

## ⏱️ Runtime Considerations

DeepPrep is a computationally intensive neuroimaging preprocessing pipeline. Execution time depends on available CPU resources, memory allocation, and dataset size.

For the single-subject BIDS test dataset used in this project, runtime on a CPU-based FABRIC VM is expected to be on the order of tens of minutes to a few hours.

The pipeline is executed as a multi-stage workflow (Nextflow-based), meaning:

* Progress is not strictly linear
* Some stages may complete quickly while others take significantly longer
* The terminal output may appear static for extended periods while long-running tasks execute in the background

This behavior is expected and does not indicate failure.

## 🔍 Monitoring Execution

Once the pipeline is running, progress can be monitored through a separate SSH session without interfering with execution. This is useful for long-running workflows where updates are intermittent.

Check active processes

`ps aux | grep deepprep`

Monitor system resource usage

`top`

Inspect output directory growth

`ls -lh ~/deepprep_project/output`

Continuous monitoring (recommended)

`watch -n 10 ls -lh ~/deepprep_project/output`

What each part means

* watch
    Runs a command repeatedly and refreshes the screen.
* -n 10
    Refresh every 10 seconds
* ls -lh ~/deepprep_project/output
    Lists files in your output folder in:
    * -l → detailed format (permissions, size, time)
    * -h → human-readable sizes (KB, MB, GB)

How to stop it

Just press:

`Ctrl + C`

These checks help confirm that the pipeline is actively running even if the log output in the primary terminal appears unchanged for a period of time.
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

Step 4: Create Slice Section
* Slice Name: test_slice
* SSH Keys: fabric-sliver-key

Click Create Slice when you are ready. Wait up to 2-3 minutes for the slice to provision.

Once the slice status is Green or StableOk, click the white square which is your node in your topology. Then you should be able to see the SSH Command. Click the copy icon on the SSH Command it and go to a terminal on your computer. It should look something like this, but with your unique hostname:
```
ssh -F <path to SSH config file> -i <path to private sliver key> ubuntu@2001:1948:417:7:f816:3eff:fe92:eb83
```
![alt text](<Screenshot 2026-04-08 at 19.54.12.png>)

Navigate to the folder you have your config and private sliver key in. Enter the SSH command and you should be inside the node.
![alt text](image.png)

# Part 2: Installing DeepPrep and Setting up on VM
These instructions are adapted from DeepPrep documentation: https://deepprep.readthedocs.io/en/latest/index.html

## Part 2a: Installing Docker on the VM

After successfully SSHing into the FABRIC VM, the next step is to install Docker, which is required to run DeepPrep.


### 1. Update system packages

```
sudo apt update
sudo apt upgrade -y
```

### 2. Install Docker (recommended method for FABRIC VM)

Since the VM is Ubuntu 20.04, Docker can be installed directly from the Ubuntu package manager:
`sudo apt install -y docker.io`

### 3. Start and enable Docker service
```
sudo systemctl start docker
sudo systemctl enable docker
```

### 4. Verify Docker installation

Run the following command to confirm Docker is working correctly:
`docker run hello-world`


### 4.1 Fixing Docker Permission Denied Error

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

Notes

* You must log out and log back in for the group change to persist across sessions.
* If Docker was installed correctly, this issue is purely a permissions configuration problem, not an installation failure.
* For time-sensitive setups (e.g., running DeepPrep), using sudo docker ... is sufficient.


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
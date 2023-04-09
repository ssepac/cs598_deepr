# cs598_deepr

This repository attempts to replicate the model and results as outlined by [Deepr: A Convolutional Net for Medical Records](https://arxiv.org/abs/1607.07519). Unlike the original paper, which uses the data of 300K patients from an Austrailian hospital chain, the reproduction here uses the [MIMIC-III dataset](https://physionet.org/content/mimiciii/1.4/).

## Setup

The code here will assume that the MIMIC-III dataset is present in a S3 bucket on AWS. Thus, the proper credentials must be suplied in an `.env` file at the root of this project and adequate permissions in AWS must be configured by the user.

- Create a new file at the root directory called `.env` and copy and paste in the contents of `.env.sample`, and assign values to these variables.
- Perform the following to download the MIMIC-III Dataset and put it in S3:
  - `brew install wget`
  - `wget -r -N -c -np --user <physionet_username> --ask-password https://physionet.org/files/mimiciii/1.4/`
  - `gunzip <your_download_location>/*`
  - Upload these files to your S3 bucket that you defined in the `.env` file
    - `aws s3 cp <your_download_location> s3://<your_bucket_name>/ --recursive`
  - Ensure adequate permissions are set up in AWS such that S3 may be accessed via the `boto3` sdk. 
- Run the Jupyter Notebook locally or in Amazon Sagemaker
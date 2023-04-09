# cs598_deepr

## Setup
- Create a new file at the root directory called `.env` and copy and paste in the contents of `.env.sample`, and assign values to these variables.
- Download the MIMIC-III Dataset and put it in S3. Run the following:
  - brew install wget
  - wget -r -N -c -np --user <physionet_username> --ask-password https://physionet.org/files/mimiciii/1.4/
  - gzip your_download_location/*
  - Upload these files to your S3 bucket that you defined in the `.env` file
- Run the Jupyter Notebook locally or in Amazon Sagemaker
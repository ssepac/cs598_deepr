# cs598_deepr

This repository attempts to replicate the model and results as outlined by [Deepr: A Convolutional Net for Medical Records](https://arxiv.org/abs/1607.07519). Unlike the original paper, which uses the data of 300K patients from an Austrailian hospital chain, the reproduction here uses the [MIMIC-III dataset](https://physionet.org/content/mimiciii/1.4/).

## Setup

### Running the Deepr Model

The code requires several CSV files from the MIMIC-III dataset in order to run. Create a folder called `mimic3` and add it to the root of the project, then add the following files from the MIMIC-III dataset: ADMISSIONS.csv, D_ICD_DIAGNOSES.csv, D_ICD_PROCEDURES.csv, DIAGNOSES_ICD.csv, PATIENTS.csv, PROCEDURES_ICD.csv, and TRANSFERS.csv.

To run the model, run all cells in the Jupyter Notebook *except* the last cell (Training and Validation). Given that we experimented with several modifications of Deepr (Deepr with a CNN, Deepr with an RNN with and without attention, and Deepr with and without embedding layers), you can set the `with_cnn`, `with_attn` and `with_embedding` to `True/False` depending on the model to be run. The original Deepr implementation has `with_cnn=True` and `with_embedding=True`. After ensuring that the desired configuration is set, you may now run the cell.

### Visualizing Motifs (optional)

After running the Deepr model with CNN, a file called `motifs_data.json` will be output to the data folder. Each object in this json file represents an EMR for a given patient. Copy the `sentence` and `normalized_motif_values` values from a given EMR and add it to the `motifs_view.html` file and update the variable assignments in the TODO sections. Open the `motifs_view.html` file to view the motifs relative to the strength of their relative filter response.
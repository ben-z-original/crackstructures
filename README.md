# CrackStructures and CrackEnsembles: <br>The Power of Multi-View for 2.5D Crack Detection

This repo contains the resources (and pointers to resources) related to our WACV'25 publication on 2.5D crack detection.

If you find our work helpful, kindly cite accordingly:
```
@inproceedings{benz2025crackstructures,
   author = {Christian Benz and Volker Rodehorst},
   booktitle = {2025 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)},
   title = {CrackStructures and CrackEnsembles: The Power of Multi-View for 2.5D Crack Detection},
   year = {2025},
}
```
The relevant components are:
- **CrackStructures**: a dataset consisting of 15 (or 18, if you count the crackless) segments from five (or six) distinct real-world structures. Offered in the repo, you are currently inspecting.
- **[CrackEnsembles](https://github.com/ben-z-original/crackensembles)**: a semi-synthetic dataset combining synthetic geometry with real-world crack images/texture.
- **[nnU-CrackNet]()**: the image-level crack segmentation model, which is a slightly improved version of the [OmniCrack30k Model]().
- **[ENSTRECT](https://github.com/ben-z-original/enstrect)**: a framework of backprojecting image-level information onto a point cloud.

## CrackStructures
CrackStructures is a dataset of real-world structures for structural crack and damage inspection.

### Overview
The dataset consists of 18 segments, three from each of six distinct structures. The segments from Bridge G only features spalling and corrosion (no cracks), but — due to the relation to structural inspection — are shipped with CrackStructures (see [ENSTRECT](https://github.com/ben-z-original/enstrect) for further detail).

![image](https://github.com/user-attachments/assets/4e8bcf4e-6cb5-45be-9228-5b7e53367b91)

### Download
The CrackStructures dataset can be downloaded:
- from [Google Drive](https://drive.google.com/file/d/1-zlLnlnHSvTrb69HQbATb7LrAAu4v5kc/view?usp=drive_link) or
- by running from the repository's root directory:
  ```bash
  pip install .
  python -m crackstructures.download
  ```

## CrackEnsembles

## nnU-CrackNet

## Enstrect


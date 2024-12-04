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
The relevant resources are:
- **CrackStructures**: a dataset consisting of 15 (or 18, if you count the crackless) segments from five (or six) distinct real-world structures. Offered in the repo, you are currently inspecting.
- **[CrackEnsembles](https://github.com/ben-z-original/crackensembles)**: a semi-synthetic dataset combining synthetic geometry with real-world crack images/texture.
- **[OmniCrack30k Model](https://github.com/ben-z-original/omnicrack30k)**: the SOTA image-level crack segmentation model.
- **[ENSTRECT](https://github.com/ben-z-original/enstrect)**: a framework of backprojecting image-level information onto a point cloud.

## CrackStructures
CrackStructures is a dataset of real-world structures for structural crack and damage inspection.

### Overview
The dataset consists of 18 segments, three from each of six distinct structures. The segments from Bridge G only features spalling and corrosion (no cracks), but — due to the relation to structural inspection — are shipped with CrackStructures (see [ENSTRECT](https://github.com/ben-z-original/enstrect) for further detail).

![image](https://github.com/user-attachments/assets/4e8bcf4e-6cb5-45be-9228-5b7e53367b91)

### Download
The CrackStructures dataset can be downloaded:
- from [Google Drive](https://drive.google.com/file/d/1-zlLnlnHSvTrb69HQbATb7LrAAu4v5kc/view?usp=drive_link)
<!--
- by running from the repository's root directory:
  ```bash
  pip install .
  python -m crackstructures.download
  ```
  -->

## CrackEnsembles
CrackEnsembles is a semi-synthetic dataset combining synthetic geometry with real-world crack images/texture. For further details and download see here [CrackEnsembles](https://github.com/ben-z-original/crackensembles).
![sample](https://github.com/user-attachments/assets/bd44b1db-f6e2-4231-b3f4-8070b736e2fb)

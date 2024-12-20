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
- **CrackEnsembles**: a semi-synthetic dataset combining synthetic geometry with real-world crack images/texture. Offered in the repo, you are currently inspecting.
- **[OmniCrack30k Model](https://github.com/ben-z-original/omnicrack30k)**: SOTA image-level crack segmentation model.
- **[ENSTRECT](https://github.com/ben-z-original/enstrect)**: framework of projecting image-level information onto a point cloud.

## CrackStructures
CrackStructures is a dataset of real-world structures for structural crack and damage inspection.
The dataset consists of 18 segments, three from each of six distinct structures. The segments from Bridge G only features spalling and corrosion (no cracks), but — due to the relation to structural inspection — are shipped with CrackStructures (see [ENSTRECT](https://github.com/ben-z-original/enstrect) for further detail).

![image](https://github.com/user-attachments/assets/4e8bcf4e-6cb5-45be-9228-5b7e53367b91)

<!--### Download
The CrackStructures dataset can be downloaded from [Google Drive](https://drive.google.com/file/d/1-zlLnlnHSvTrb69HQbATb7LrAAu4v5kc/view?usp=drive_link)

- by running from the repository's root directory:
  ```bash
  pip install .
  python -m crackstructures.download
  ```
  -->

## CrackEnsembles
CrackEnsembles is a semi-synthetic dataset combining synthetic geometry with real-world crack images/texture.
![sample](https://github.com/user-attachments/assets/bd44b1db-f6e2-4231-b3f4-8070b736e2fb)
The dataset is procedurally created by
1. Picking three geometric primitives (from a set of four primitives, cube, tetrahedron, cylinder, and sphere).
2. Randomizing the position and scale of the single primitives and combining them into one mesh.
3. Selecting four images from a crack datasets and stitching them into a 2048x2048 texture map. For unrestricted distribution of CrackEnsembles images only from the S2DS, UAV75, and Khanh dataset were considered. For more datasets and details see [OmniCrack30k](https://github.com/ben-z-original/omnicrack30k).
4. Randomizing 32 extrinsics around the mesh and rendering views using the PyTorch3D mesh renderer.
5. Inferring the ground truth medial axes of the cracks in 3D space by using point cloud contraction (for details see [ENSTRECT](https://github.com/ben-z-original/enstrect)).

## Downloads
The datasets can be downloaded from:
- **CrackStructures**: [Google Drive](https://drive.google.com/file/d/1-zlLnlnHSvTrb69HQbATb7LrAAu4v5kc/view?usp=drive_link)
- **CrackEnsembles**: [Google Drive](https://drive.google.com/file/d/13_-0uF0inOyw4iemlpop-O0iISid0o8e/view?usp=sharing) (Training and test sets are being processed and added soon).

## References
```
@inproceedings{benz2025crackstructures,
   author = {Christian Benz and Volker Rodehorst},
   title = {CrackStructures and CrackEnsembles: The Power of Multi-View for 2.5D Crack Detection},
   booktitle = {2025 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)},
   year = {2025}
}

@inproceedings{benz2025enstrect,
   author = {Christian Benz and Volker Rodehorst},
   title = {Enstrect: A Stage-based Approach to 2.5D Structural Damage Detection},
   booktitle = {Computer Vision -- ECCV 2024 Workshops},
   publisher = {Springer},
   city = {Cham},
   year = {2025}
}

@inproceedings{benz2024omnicrack30k,
   author = {Christian Benz and Volker Rodehorst},
   title = {OmniCrack30k: A Benchmark for Crack Segmentation and the Reasonable Effectiveness of Transfer Learning},
   booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) Workshops},
   pages = {3876-3886},
   year = {2024}
}

@inproceedings{benz2022image,
   author = {Christian Benz and Volker Rodehorst},
   title = {Image-based Detection of Structural Defects using Hierarchical Multi-scale Attention},
   booktitle = {Pattern Recognition. DAGM GCPR 2022. Lecture Notes in Computer Science, vol 13485},
   editor = {Björn Andres and Florian Bernard and Daniel Cremers and Simone Frintrop and Bastian Goldlücke and Ivo Ihrke},
   pages = {337-353},
   publisher = {Springer},
   city = {Cham},
   year = {2022}
}

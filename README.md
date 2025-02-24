# CrackStructures and CrackEnsembles: <br>The Power of Multi-View for 2.5D Crack Detection

## ${\color{red}\textsf{Under Construction: Likely ready by Sat, March 1, 2025.}}$
This repo contains the resources (and pointers to resources) related to our WACV'25 publication on 2.5D crack detection.

<p align="center">
    <img src="https://github.com/user-attachments/assets/ad461027-aa39-47c9-b561-170569cc7d0c" width=40% alt="Indoors segment"> 
    <img src="https://github.com/user-attachments/assets/a6cf3236-f984-4c83-a73f-954cf712faaa" width=50% alt="Predictions">
</p>

The relevant resources are:
- **CrackStructures**: a dataset consisting of 15 (resp. 18, if you count the crackless) segments from five (resp. six) distinct real-world structures. Offered in the repo, you are currently inspecting.
- **CrackEnsembles**: a semi-synthetic dataset combining synthetic geometry with real-world crack images/texture. Offered in the repo, you are currently inspecting.
- **[OmniCrack30k Model](https://github.com/ben-z-original/omnicrack30k)**: SOTA image-level crack segmentation model.
- **[ENSTRECT](https://github.com/ben-z-original/enstrect)**: framework of projecting image-level information onto a point cloud.

## Citation
[Link to WACV'25 Paper](https://openaccess.thecvf.com/content/WACV2025/papers/Benz_CrackStructures_and_CrackEnsembles_The_Power_of_Multi-View_for_2.5D_Crack_WACV_2025_paper.pdf)

If you find our work useful, kindly cite accordingly:
```
@InProceedings{Benz_2025_WACV,
    author    = {Benz, Christian and Rodehorst, Volker},
    title     = {CrackStructures and CrackEnsembles: The Power of Multi-View for 2.5D Crack Detection},
    booktitle = {Proceedings of the Winter Conference on Applications of Computer Vision (WACV)},
    month     = {February},
    year      = {2025},
    pages     = {5990-5999}
}
```


## Installation
The repo can be installed by:
```
# create and activate conda environment
conda create --name crackstructures python=3.10
conda activate crackstructures

# install and build repository
pip install -e .
pip install git+https://github.com/facebookresearch/pytorch3d.git@v0.7.7  # needs knowledge about installed torch version
```
The PyTorch3D dependency can be itchy. Also refer to [PyTorch3D Issues](https://github.com/ben-z-original/enstrect/tree/main?tab=readme-ov-file#pytorch3d-issues) in ENSTRECT.

## Data
### Data Download
The datasets can be downloaded:
- by running (which places the dataset correctly in the repo tree)
   - **CrackStructures**: ```python -m crackstructures.datasets.download crackstructures```
   - **CrackEnsembles**: ```python -m crackstructures.datasets.download crackensembles```
     
- or manually (correct placement in repo tree required, see below).
    - **CrackStructures**: [Google Drive](https://drive.google.com/file/d/1-zlLnlnHSvTrb69HQbATb7LrAAu4v5kc/view?usp=drive_link)
    - **CrackEnsembles**: [Google Drive](https://drive.google.com/file/d/13_-0uF0inOyw4iemlpop-O0iISid0o8e/view?usp=sharing) (Training and test sets are being processed and added soon).

### Data Organization
For running the example, it must be corretly placed in the assets folder in the repository tree:
```
└── crackstructures
    ├── ...
    └── src
        └── crackstructures
            ├── ...
            └── assets
                └── crackstructures  # <-here it goes (unzipped)
```

### Camera Representation
For the (custom, but straightforward) camera representation, kindly refer to [Camera Representation](https://github.com/ben-z-original/enstrect/tree/main?tab=readme-ov-file#custom-data) in ENSTRECT.

## Run Example
With the data placed in the right path, the example can be run. It uses image scale 0.25 for reduced runtime; for better quality change the ```--scale``` parameter to 1.0. For the default parameters run:
```
python -m crackstructures.run
```
With custom parameters run e.g. (from the repo's root path):
```
python -m crackstructures.run \
    --obj_or_ply_path src/crackstructures/assets/crackstructures/indoors/segment3/mesh/mesh.obj \
    --images_dir src/crackstructures/assets/crackstructures/indoors/segment3/views \
    --cameras_path src/crackstructures/assets/crackstructures/indoors/segment3/cameras.json \
    --out_dir src/crackstructures/assets/crackstructures/indoors/segment3/out \
    --scale 0.5 \
    --num_points 1000000
```

## Evaluation
The evaluation assumed the following directory structure:
```
indoors
└── segment3
    ├── annotations
    │   └── crack.obj                  # <- manually labeled cracks (with CloudCompare "Trace Polyline" function and converted to obj)
    ├── cameras.json                   # <- camera information in custom format (see above)
    ├── mesh
    │   ├── ...
    │   └── mesh.obj                   # <- obj with texture
    ├── out
    │   ├── crack.obj                  # <- obj with predicted cracks
    │   └── pcd_1000000_processed.ply  # <- segmented point cloud (see, e.g., attributes "crack" or "argmax")
    └── views                          # <- the images
        ├── 0000.jpg
        ├── 0001.jpg
        └── ...
```

Given this directory structure run:
```
python -m crackstructures.evaluation.run \
    --datadir src/crackstructures/assets/crackstructures \
    --structure indoors \
    --segment segment3 \
    --vis

# out:
#   Tol 	 IoU
#   0.005    0.627
#   0.01     0.684
#   0.02     0.721
#   0.04     0.721
#   0.08     0.815
```
The clCloudIoUs corresponding to the tolerances will be provided in the terminal, an interactive plot is shown.


## CrackStructures
CrackStructures is a dataset of real-world structures for structural crack and damage inspection.
The dataset consists of 18 segments, three from each of six distinct structures. The segments from Bridge G only features spalling and corrosion (no cracks), but — due to the relation to structural inspection — are shipped with CrackStructures (see [ENSTRECT](https://github.com/ben-z-original/enstrect) for further detail).

<p align="center">
<img src="https://github.com/user-attachments/assets/4e8bcf4e-6cb5-45be-9228-5b7e53367b91" width=50% alt="CrackStructures">
</p>

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

<p align="center">
<img src="https://github.com/user-attachments/assets/bd44b1db-f6e2-4231-b3f4-8070b736e2fb" width=80% alt="CrackEnsembles">
</p>

The dataset is procedurally created by
1. Picking three geometric primitives (from a set of four primitives, cube, tetrahedron, cylinder, and sphere).
2. Randomizing the position and scale of the single primitives and combining them into one mesh.
3. Selecting four images from a crack datasets and stitching them into a 2048x2048 texture map. For unrestricted distribution of CrackEnsembles images only from the S2DS, UAV75, and Khanh dataset were considered. For more datasets and details see [OmniCrack30k](https://github.com/ben-z-original/omnicrack30k).
4. Randomizing 32 extrinsics around the mesh and rendering views using the PyTorch3D mesh renderer.
5. Inferring the ground truth medial axes of the cracks in 3D space by using point cloud contraction (for details see [ENSTRECT](https://github.com/ben-z-original/enstrect)).



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

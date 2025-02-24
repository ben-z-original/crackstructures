import argparse
import numpy as np
from pathlib import Path
from pytorch3d.io import IO
from tensordict import TensorDict
from torch.utils.data import Dataset
from torchvision.utils import save_image
from enstrect.extraction.utils import G_to_obj
from crackstructures.utils.visualization import scene_pyt3d_to_gif
from crackstructures.datasets.geometries.create import sample_geometry, add_textures
from crackstructures.utils.conversion import cameras_pyt3d_to_json, mesh_o3d_to_pyt3d
from crackstructures.datasets.utils import PyTorch3DMeshRenderer, sample_extrinsics, generate_annotation


class CrackEnsemblesDataset(Dataset):
    def __init__(self, image_paths, centerline_paths, num_cameras, image_size=(256, 256),
                 out_dir=None, start_idx=0, create_gif=False, device="cuda:0"):
        self.image_paths = image_paths
        self.centerline_paths = centerline_paths
        self.num_cameras = num_cameras
        self.image_size = image_size
        self.out_dir = out_dir
        self.start_idx = start_idx
        self.create_gif = create_gif
        self.device = device

        self.out_dir.mkdir(exist_ok=True, parents=True)
        self.renderer = PyTorch3DMeshRenderer(image_size=self.image_size)

    def __len__(self):
        return len(self.image_paths) // 4

    def __getitem__(self, idx):
        np.random.seed(idx + self.start_idx)

        # sample geometry
        geom_combined, geoms_list = sample_geometry()

        # add textures
        images = self.image_paths[idx * 4:idx * 4 + 4]
        labels = self.centerline_paths[idx * 4:idx * 4 + 4]
        geom_combined, texture_img, texture_lab = add_textures(geom_combined, images, labels)
        mesh_pyt3d = mesh_o3d_to_pyt3d(geom_combined).to(self.device)

        # sample cameras and render views
        np.random.seed(idx + self.start_idx)
        cameras = sample_extrinsics(mesh=mesh_pyt3d, num_cameras=self.num_cameras, image_size=self.image_size)
        views = self.renderer(mesh_pyt3d, cameras)

        # generate annotation
        G, pcd_pynt = generate_annotation(mesh_pyt3d.clone(), texture_lab, geoms_list)

        # store results
        if self.out_dir is not None:
            # prepare paths
            sample_dir = self.out_dir / f"{idx + self.start_idx:04d}"
            annotations_dir = sample_dir / "annotations"
            mesh_dir = sample_dir / "mesh"
            views_dir = sample_dir / "views"

            # create directories
            annotations_dir.mkdir(exist_ok=True, parents=True)
            mesh_dir.mkdir(exist_ok=True)
            views_dir.mkdir(exist_ok=True)

            # save cameras
            view_keys = [f"{key:04d}" for key in range(len(cameras))]
            cameras_pyt3d_to_json(view_keys, cameras, sample_dir / "cameras.json")

            # save views
            for j, view in enumerate(views):
                save_image(view.moveaxis(-1, 0), views_dir / f"{j:04d}.png")

            # save mesh
            IO().save_mesh(mesh_pyt3d, mesh_dir / "mesh.obj")
            pcd_pynt.to_file(str(mesh_dir / "pcd.ply"))

            # save annotations
            G_to_obj(G, annotations_dir / "crack.obj")

            if self.create_gif:
                gif_path = str(sample_dir / "sample.gif")
                scene_pyt3d_to_gif(mesh_pyt3d, texture_img, G, gif_path, cameras)

        tensor_dict = {"cameras": cameras,
                       "views": views,
                       "mesh": mesh_pyt3d}
        return TensorDict(tensor_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crack Ensembles Dataset Generation")
    parser.add_argument('--images_dir', type=Path, required=True,
                        help='Directory containing the images')
    parser.add_argument('--centerlines_dir', type=Path, required=True,
                        help='Directory containing the centerline labels')
    parser.add_argument('--out_dir', type=Path, required=True,
                        help='Output directory for the generated dataset')
    parser.add_argument('--num_cameras', type=int, default=32, help='Number of cameras to sample')
    parser.add_argument('--start_idx', type=int, default=0, help='Starting index for the dataset')
    parser.add_argument('--filter_images', action='store_true',
                        help='Remove images not in UAV*, S2DS*, or Khanh*')
    parser.add_argument('--create_gif', action='store_true', help='Create GIF for each sample')
    args = parser.parse_args()

    np.random.seed(42)

    # images and labels
    if args.filter_images:
        img_paths = list(sorted(args.images_dir.glob("UAV*.png")))
        img_paths.extend(list(sorted(args.images_dir.glob("S2DS*.png"))))
        img_paths.extend(list(sorted(args.images_dir.glob("Khanh*.png"))))
    else:
        img_paths = list(sorted(args.images_dir.glob("*")))

    img_paths = np.random.permutation(np.array(img_paths))
    lab_paths = np.array([args.centerlines_dir / f.name for f in img_paths])

    dataset = CrackEnsemblesDataset(image_paths=img_paths, centerline_paths=lab_paths, num_cameras=args.num_cameras,
                                    out_dir=args.out_dir, start_idx=args.start_idx, create_gif=args.create_gif)

    for idx, sample in enumerate(dataset):
        print(f"Generated sample {idx + args.start_idx:04d}")

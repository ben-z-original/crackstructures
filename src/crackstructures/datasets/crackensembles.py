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
    def __init__(self, img_paths, lab_paths, num_cameras, image_size=(256, 256),
                 out_path=None, start_idx=0, device="cuda:0"):
        self.img_paths = img_paths
        self.lab_paths = lab_paths
        self.num_cameras = num_cameras
        self.image_size = image_size
        self.out_path = out_path
        self.start_idx = start_idx
        self.device = device

        self.out_path.mkdir(exist_ok=True, parents=True)
        self.renderer = PyTorch3DMeshRenderer(image_size=self.image_size)

    def __len__(self):
        return len(self.img_paths) // 4

    def __getitem__(self, idx, create_gif=True):
        np.random.seed(idx + self.start_idx)

        # sample geometry
        geom_combined, geoms_list = sample_geometry()

        # add textures
        images = self.img_paths[idx * 4:idx * 4 + 4]
        labels = self.lab_paths[idx * 4:idx * 4 + 4]
        geom_combined, texture_img, texture_lab = add_textures(geom_combined, images, labels)
        mesh_pyt3d = mesh_o3d_to_pyt3d(geom_combined).to(self.device)

        # sample cameras and render views
        np.random.seed(idx + self.start_idx)
        cameras = sample_extrinsics(mesh=mesh_pyt3d, num_cameras=self.num_cameras, image_size=self.image_size)
        views = self.renderer(mesh_pyt3d, cameras)

        # generate annotation
        G, pcd_pynt = generate_annotation(mesh_pyt3d.clone(), texture_lab, geoms_list)

        # store results
        if self.out_path is not None:
            # prepare paths
            sample_path = self.out_path / f"{idx + self.start_idx:04d}"
            annotations_path = sample_path / "annotations"
            mesh_path = sample_path / "mesh"
            views_path = sample_path / "views"

            # create directories
            annotations_path.mkdir(exist_ok=True, parents=True)
            mesh_path.mkdir(exist_ok=True)
            views_path.mkdir(exist_ok=True)

            # save cameras
            view_keys = [f"{key:04d}" for key in range(len(cameras))]
            cameras_pyt3d_to_json(view_keys, cameras, sample_path / "cameras.json")

            # save views
            for j, view in enumerate(views):
                save_image(view.moveaxis(-1, 0), views_path / f"{j:04d}.png")

            # save mesh
            IO().save_mesh(mesh_pyt3d, mesh_path / "mesh.obj")
            pcd_pynt.to_file(str(mesh_path / "pcd.ply"))

            # save annotations
            G_to_obj(G, annotations_path / "crack.obj")

            if create_gif:
                gif_path = str(sample_path / "sample.gif")
                scene_pyt3d_to_gif(mesh_pyt3d, texture_img, G, gif_path, cameras)

        tensor_dict = {"cameras": cameras,
                       "views": views,
                       "mesh": mesh_pyt3d}
        return TensorDict(tensor_dict)


if __name__ == "__main__":
    # images and labels
    np.random.seed(42)
    img_paths = list(sorted(img_dir.glob("UAV*.png")))
    img_paths.extend(list(sorted(img_dir.glob("S2DS*.png"))))
    img_paths.extend(list(sorted(img_dir.glob("Khanh*.png"))))
    img_paths = np.random.permutation(np.array(img_paths))
    lab_paths = np.array([lab_dir / f.name for f in img_paths])


    start_idx = 1090
    dataset = CrackEnsemblesDataset(img_paths=img_paths, lab_paths=lab_paths,
                                    num_cameras=32, out_path=out_path, start_idx=start_idx)
    for sample in enumerate(dataset):
        print()

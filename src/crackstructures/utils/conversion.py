import json
import torch
import numpy as np
import pandas as pd
import pyvista as pv
from pyntcloud import PyntCloud
from pytorch3d.renderer import TexturesUV
from pytorch3d.structures import Meshes


def mesh_o3d_to_pyt3d(mesh_o3d):
    verts = torch.tensor(np.array(mesh_o3d.vertices), dtype=torch.float32)
    faces = torch.tensor(np.array(mesh_o3d.triangles))
    verts_uvs = torch.tensor(np.array(mesh_o3d.triangle_uvs), dtype=torch.float32)
    faces_uvs = torch.arange(len(verts_uvs)).reshape(-1, 3)
    texture_img = torch.tensor(np.copy(np.array(mesh_o3d.textures)[0, ::-1]), dtype=torch.float32) / 255

    texture = TexturesUV(verts_uvs=[verts_uvs], faces_uvs=[faces_uvs], maps=[texture_img])
    mesh_pyt3d = Meshes(verts=[verts], faces=[faces], textures=texture)

    return mesh_pyt3d


def mesh_pyt3d_to_pv(mesh_pyt3d):
    # geometry
    vertices = np.array(mesh_pyt3d.verts_packed().cpu()[mesh_pyt3d.faces_packed().cpu()].reshape(-1, 3))
    faces = np.arange(0, len(vertices)).reshape(-1, 3)
    mesh_pv = pv.PolyData.from_regular_faces(vertices, faces)

    # texture
    mesh_pv.active_texture_coordinates = np.array(
        mesh_pyt3d.textures.verts_uvs_padded().cpu()[0, mesh_pyt3d.textures.faces_uvs_padded().cpu()[0]].reshape(-1, 2))
    texture = pv.numpy_to_texture(np.uint8(255 * np.array(mesh_pyt3d.textures.maps_padded().squeeze().cpu())))
    return mesh_pv, texture


def pointcloud_pyt3d_to_pynt(pcd_pyt3d):
    points_pd = pd.DataFrame(torch.cat([pcd_pyt3d.points_packed().squeeze(),
                                        pcd_pyt3d.normals_packed().squeeze(),
                                        pcd_pyt3d.features_packed().squeeze()], axis=1),
                             columns=["x", "y", "z", "nx", "ny", "nz", "red", "green", "blue"])
    pcd_pynt = PyntCloud(points_pd)
    return pcd_pynt


def cameras_pyt3d_to_json(view_keys, cameras, outpath):
    cameras_dict = {key: {"focal_length": cam.focal_length.cpu().numpy().tolist(),
                          "principal_point": cam.principal_point.cpu().numpy().tolist(),
                          "image_size": cam.image_size.cpu().numpy().tolist(),
                          "R": cam.R.cpu().numpy().tolist(),
                          "T": cam.T.cpu().numpy().tolist(),
                          "in_ndc": cam.in_ndc()} for key, cam in zip(view_keys, cameras)}
    with open(outpath, 'w') as f:
        json.dump(cameras_dict, f, indent=2)

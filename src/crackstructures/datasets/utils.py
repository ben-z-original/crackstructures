import json
import torch
import numpy as np
import open3d as o3d
from enstrect.extraction.contraction import extract_centerlines
from enstrect.datasets.utils import sample_points_from_meshes_pyt3d
from crackstructures.utils.conversion import pointcloud_pyt3d_to_pynt
from pytorch3d.renderer import (look_at_view_transform, PerspectiveCameras, PointLights, MeshRenderer,
                                MeshRasterizer, RasterizationSettings, HardPhongShader)


def normalize_geom(geom):
    mins = geom.get_min_bound()
    maxs = geom.get_max_bound()
    extensions = maxs - mins
    center = (mins + maxs) / 2
    geom.translate(-center)
    geom.scale(1 / max(extensions), center=[0, 0, 0])
    return geom


class PyTorch3DMeshRenderer:
    def __init__(self, image_size=(256, 256), device="cuda"):
        lights = PointLights(ambient_color=((0.9, 0.9, 0.9),),
                             diffuse_color=((0.8, 0.8, 0.8),),
                             specular_color=((0.0, 0.0, 0.0),),
                             location=((10, 0, 0),),
                             device=device)

        self.renderer = MeshRenderer(
            rasterizer=MeshRasterizer(
                raster_settings=RasterizationSettings(
                    image_size=image_size,
                    blur_radius=0.0,
                    faces_per_pixel=1,
                )
            ),
            shader=HardPhongShader(
                device=device,
                lights=lights
            )
        )

    def __call__(self, mesh, cameras):
        views = self.renderer(mesh.extend(len(cameras)), cameras=cameras)
        return views


def sample_extrinsics(image_size=(256, 256), mesh=None, num_cameras=32, distance=1):
    device = mesh.device
    at = [[0, 0, 0]] if mesh is None else \
        mesh.get_bounding_boxes().mean(dim=-1) + (torch.rand((num_cameras, 1), device=device) - 0.5) * 0.1

    # distance
    dist = distance + np.random.rand(num_cameras)
    # elevation
    x = np.linspace(-np.pi / 2, np.pi / 2, num_cameras)
    elev = np.sign(x) * (1 - np.cos(x)) * 90
    # azimuth
    azim = np.random.permutation(np.linspace(0, 360, num_cameras, endpoint=False))

    R, T = look_at_view_transform(dist=dist, elev=elev, azim=azim, at=at)

    cameras = PerspectiveCameras(device=device, R=R, T=T,
                                 image_size=(image_size,),
                                 focal_length=((300, 300),),  # 2000
                                 principal_point=(np.asarray(image_size)[::-1] / 2.0,),
                                 in_ndc=False)

    return cameras


def generate_annotation(mesh_pyt3d, texture_lab, geoms_list):
    texture_lab_pyt3d = torch.tensor(np.copy(texture_lab[::-1]), dtype=torch.float32) / 255
    mesh_pyt3d.textures._maps_padded = texture_lab_pyt3d[None]

    # sample point cloud
    pcd_pyt3d = sample_points_from_meshes_pyt3d(mesh_pyt3d, num_points=2000000)
    pcd_pynt = pointcloud_pyt3d_to_pynt(pcd_pyt3d.cpu())
    pcd_pynt.points["crack"] = np.ubyte(pcd_pynt.points["red"] > 0)

    # remove points inside geometry
    for geom in geoms_list:
        mesh = o3d.t.geometry.TriangleMesh.from_legacy(geom)
        scene = o3d.t.geometry.RaycastingScene()
        scene.add_triangles(mesh)
        distances = scene.compute_signed_distance(
            o3d.core.Tensor(np.array(pcd_pynt.points[["x", "y", "z"]]))).numpy()
        pcd_pynt.points = pcd_pynt.points[distances >= -0.001]
        pcd_pynt.points.reset_index(drop=True, inplace=True)

    G = extract_centerlines(pcd_pynt, category="crack",
                            eps_m=0.03, min_points=2, min_samples_cluster=1, init_contraction=1.)
    return G, pcd_pynt

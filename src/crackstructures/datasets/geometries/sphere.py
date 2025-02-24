import torch
import numpy as np
import open3d as o3d
from scipy.spatial.transform import Rotation
from crackstructures.datasets.utils import normalize_geom


def adjust_sphere_uvs(triangle_uvs_side, flip_uv=False):
    triangle_uvs_side = triangle_uvs_side[:, [1, 0]] if flip_uv else triangle_uvs_side
    triangle_uvs_side = torch.round(triangle_uvs_side, decimals=4)
    source_y = triangle_uvs_side[:, 1].unique()
    target = torch.linspace(0, 1, len(source_y), dtype=torch.float64)

    for ii, src_y in enumerate(source_y):
        idxs = torch.where(triangle_uvs_side[:, 1] == src_y)[0]
        for jj, src_x in enumerate(triangle_uvs_side[idxs, 0].unique()):
            idxs_x = torch.where(triangle_uvs_side[idxs, 0] == src_x)[0]
            iii = idxs[idxs_x]
            triangle_uvs_side[iii, :] = torch.stack([target[jj], target[ii]])

    triangle_uvs_side[:, 0] = 1 - triangle_uvs_side[:, 0] if flip_uv else triangle_uvs_side[:, 0]
    triangle_uvs_side[:, 1] = 1 - triangle_uvs_side[:, 1] if flip_uv else triangle_uvs_side[:, 1]

    return triangle_uvs_side


def prepare_sphere():
    # adapted cube map approach

    # create geometry
    geom = o3d.geometry.TriangleMesh.create_sphere(create_uv_map=True)
    geom = normalize_geom(geom)

    triangle_verts = torch.tensor(np.array(geom.vertices)[np.array(geom.triangles).flatten()], dtype=torch.float64)
    triangle_center = triangle_verts.reshape(-1, 3, 3).mean(axis=1)

    # assign sphere vertices to cube side
    cluster_centroids_topbottom = torch.tensor([
        # left, right, back, front, bottom, top
        [-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, -1], [0, 0, 1],
        # diagonals (for assignment disambiguation)
        [-0.7, -0.7, 0], [0.7, -0.7, 0], [-0.7, 0.7, 0], [0.7, 0.7, 0],
    ], dtype=torch.float64)

    cluster_centroids_sides = torch.tensor([
        # left, right, back, front
        [-1, 0, 0, ], [1, 0, 0], [0, -1, 0], [0, 1, 0]
    ], dtype=torch.float64)

    # assign to sides
    top_or_bottom = np.argmax(torch.cdist(triangle_center, cluster_centroids_topbottom), axis=1)
    side = np.argmax(torch.cdist(triangle_center, cluster_centroids_sides), axis=1)
    side[top_or_bottom == 4] = 4
    side[top_or_bottom == 5] = 5

    # project to vertices to cube
    x, y, z = triangle_verts.T
    side = side.repeat(3, 1).T.flatten()
    triangle_uvs = torch.zeros((len(triangle_verts), 2), dtype=torch.float64)  # , device=device)
    triangle_uvs[side == 0] = (0.5 * (1 + torch.vstack((+z, -y)) / torch.abs(x))).T[side == 0]
    triangle_uvs[side == 1] = (0.5 * (1 + torch.vstack((-z, -y)) / torch.abs(x))).T[side == 1]
    triangle_uvs[side == 2] = (0.5 * (1 + torch.vstack((+x, -z)) / torch.abs(y))).T[side == 2]
    triangle_uvs[side == 3] = (0.5 * (1 + torch.vstack((+x, +z)) / torch.abs(y))).T[side == 3]
    triangle_uvs[side == 4] = (0.5 * (1 + torch.vstack((-x, -y)) / torch.abs(z))).T[side == 4]
    triangle_uvs[side == 5] = (0.5 * (1 + torch.vstack((+x, -y)) / torch.abs(z))).T[side == 5]

    # adjust texture coordinates to exploit full texture space and reduce distortion
    triangle_uvs[side == 0, :] = adjust_sphere_uvs(triangle_uvs[side == 0, :])
    triangle_uvs[side == 1, :] = adjust_sphere_uvs(triangle_uvs[side == 1, :])
    triangle_uvs[side == 2, :] = adjust_sphere_uvs(triangle_uvs[side == 2, :], flip_uv=True)
    triangle_uvs[side == 3, :] = adjust_sphere_uvs(triangle_uvs[side == 3, :], flip_uv=True)

    triangle_uvs = triangle_uvs * 0.98 + 0.01

    # shift to texture map quadrants
    triangle_uvs /= 2
    triangle_uvs[side == 1, 0] += 0.5
    triangle_uvs[side == 3, 0] += 0.5
    triangle_uvs[side == 4, 1] += 0.5
    triangle_uvs[side == 5, :] += 0.5

    geom.triangle_uvs = o3d.utility.Vector2dVector(triangle_uvs)

    # adjust rotation to avoid alignment with textures from other primitives
    R = Rotation.from_euler("xyz", [-90, 0, 0], degrees=True).as_matrix()
    geom = geom.rotate(R, center=(0, 0, 0))

    return geom

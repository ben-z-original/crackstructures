import numpy as np
import open3d as o3d
from scipy.spatial.transform import Rotation
from crackstructures.datasets.utils import normalize_geom


def prepare_cube():
    geom = o3d.geometry.TriangleMesh.create_box(create_uv_map=True)
    geom = normalize_geom(geom)

    triangle_uvs = np.array([[0.5, 0.5], [1.0, 1.0], [0.5, 1.0],
                             [0.5, 0.5], [1.0, 0.5], [1.0, 1.0],
                             [0.0, 0.5], [0.0, 0.0], [0.5, 0.5],
                             [0.0, 0.0], [0.5, 0.0], [0.5, 0.5],
                             [0.5, 0.5], [0.5, 0.0], [1.0, 0.5],
                             [0.5, 0.0], [1.0, 0.0], [1.0, 0.5],
                             [0.5, 1.0], [0.5, 0.5], [0.0, 0.5],
                             [0.5, 1.0], [0.0, 0.5], [0.0, 1.0],
                             [0.0, 0.0], [0.0, 0.5], [0.5, 0.5],
                             [0.0, 0.0], [0.5, 0.5], [0.5, 0.0],
                             [0.0, 1.0], [0.0, 0.5], [0.5, 1.0],
                             [0.5, 1.0], [0.0, 0.5], [0.5, 0.5]])
    triangle_uvs = triangle_uvs * 0.98 + 0.01

    geom.triangle_uvs = o3d.utility.Vector2dVector(triangle_uvs)

    # adjust rotation to avoid alignment with textures from other primitives
    R = Rotation.from_euler("xyz", [0, 0, 90], degrees=True).as_matrix()
    geom = geom.rotate(R, center=(0, 0, 0))

    return geom

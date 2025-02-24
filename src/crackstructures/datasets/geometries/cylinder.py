import numpy as np
import open3d as o3d
from scipy.spatial.transform import Rotation
from crackstructures.datasets.utils import normalize_geom


def prepare_cylinder():
    geom = o3d.geometry.TriangleMesh.create_cylinder(create_uv_map=True)
    geom = normalize_geom(geom)

    triangle_uvs = np.array(geom.triangle_uvs)
    triangle_uvs[3 * 40:, 0] = (triangle_uvs[3 * 40:, 0] / 2)
    geom.triangle_uvs = o3d.utility.Vector2dVector(triangle_uvs)

    # adjust rotation to avoid alignment with textures from other primitives
    R = Rotation.from_euler("xyz", [0, 180, 180], degrees=True).as_matrix()
    geom = geom.rotate(R, center=(0, 0, 0))

    return geom

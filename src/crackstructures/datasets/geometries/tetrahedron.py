import numpy as np
import open3d as o3d
from scipy.spatial.transform import Rotation
from crackstructures.datasets.utils import normalize_geom


def prepare_tetrahedron():
    geom = o3d.geometry.TriangleMesh.create_tetrahedron(create_uv_map=True)
    geom = normalize_geom(geom)

    tri_h = np.tan(np.deg2rad(60)) * (1 / 4)

    q0 = q1 = q2 = q3 = (0.5 - tri_h) / 2

    geom.triangle_uvs = o3d.utility.Vector2dVector(
        np.array([[q2, 0.5],
                  [q2 + tri_h, 0.75],
                  [q2, 1.0],

                  [1.0 - q0, 0.5],
                  [1.0 - q0, 1.0],
                  [1.0 - q0 - tri_h, 0.75],

                  [1.0 - q1, 0.0],
                  [1.0 - q1, 0.5],
                  [1.0 - q1 - tri_h, 0.25],

                  [q3, 0.5],
                  [q3, 0.0],
                  [q3 + tri_h, 0.25]]))

    # adjust rotation to avoid alignment with textures from other primitives
    R = Rotation.from_euler("xyz", [180, 0, 0], degrees=True).as_matrix()
    geom = geom.rotate(R, center=(0, 0, 0))

    return geom

import cv2
import copy
import numpy as np
import open3d as o3d
from crackstructures.datasets.utils import normalize_geom
from crackstructures.datasets.geometries.tetrahedron import prepare_tetrahedron
from crackstructures.datasets.geometries.cube import prepare_cube
from crackstructures.datasets.geometries.cylinder import prepare_cylinder
from crackstructures.datasets.geometries.sphere import prepare_sphere

geometries = [
    prepare_tetrahedron(),
    prepare_cube(),
    prepare_cylinder(),
    prepare_sphere()
]


def randomize_scale(geoms):
    for subgeom in geoms:
        subgeom = subgeom.scale(np.random.uniform(0.5, 0.8), center=(0, 0, 0))


def merge_geometries(selected):
    final_geom = copy.deepcopy(selected[0])

    for subgeom in selected[1:]:
        final_geom += subgeom

    final_geom.triangle_uvs = o3d.utility.Vector2dVector(np.concatenate([
        np.array(sel.triangle_uvs) for sel in selected], axis=0))

    return final_geom


def combines_images_to_texture(img_paths, lab_paths):
    imgs = [cv2.cvtColor(cv2.imread(str(path), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
            for path in img_paths]
    labs = [cv2.imread(str(path), cv2.IMREAD_COLOR) for path in lab_paths]

    for i, (img, lab) in enumerate(zip(imgs, labs)):
        h, w = img.shape[:2]
        lab = cv2.resize(lab, img.shape[:2])
        lab = 255 - lab
        lab[..., [1, 2]] = 0

        hc, wc = (np.array(img.shape[:2]) - min(img.shape[:2])) // 2

        imgs[i] = cv2.resize(img[hc:h - hc, wc:w - wc, :], (1024, 1024))
        labs[i] = cv2.resize(lab[hc:h - hc, wc:w - wc, :], (1024, 1024), interpolation=cv2.INTER_NEAREST)

    imgs = np.vstack([np.hstack(imgs[0:2]), np.hstack(imgs[2:4])])
    labs = np.vstack([np.hstack(labs[0:2]), np.hstack(labs[2:4])])

    return imgs, labs


def sample_geometry():
    # choose base and supplementary geometries
    base_choice = np.random.choice([0, 1])
    base_geom = geometries[base_choice]
    geoms = np.random.choice(geometries[base_choice + 1:], 2, replace=False)
    geoms = [normalize_geom(geom) for geom in geoms]

    # randomize scale and shift
    randomize_scale(geoms)
    anchors = np.random.permutation(np.array(base_geom.vertices))[:len(geoms)]
    geoms = [base_geom] + [geom.translate(anchors[j]) for j, geom in enumerate(geoms)]

    # combine into single mesh
    geom_combined = merge_geometries(geoms)

    return geom_combined, geoms


def add_textures(geom_combined, images, labels):
    texture_img, texture_lab = combines_images_to_texture(images, labels)
    geom_combined.textures = [o3d.geometry.Image(texture_img)]

    return geom_combined, texture_img, texture_lab

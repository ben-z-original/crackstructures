import numpy as np
import pyvista as pv
from time import sleep
from pytorch3d.renderer import PerspectiveCameras
from enstrect.extraction.utils import G_to_lineset_o3d
from crackstructures.utils.conversion import mesh_pyt3d_to_pv


def add_cameras(pl: pv.Plotter, cameras: PerspectiveCameras) -> None:
    """
    Add pytorch3d cameras to pyvista plot.

    :param pl: pyvista plotter
    :param cameras: pytorch3d cameras
    """
    camera = pv.Camera()
    camera.clipping_range = (0.0001, 0.25)  # 0.5)
    for cam in cameras:
        h, w = cam.image_size.squeeze()
        frustum = camera.view_frustum((w / h).item())
        frustum.points = frustum.points - [0, 0, 1]  # to center
        frustum.points = frustum.points * [1, 1, -1]  # from -z to +z
        frustum.points @= cam.get_world_to_view_transform().inverse().get_matrix()[0, :3, :3].cpu().numpy()
        frustum.points += cam.get_world_to_view_transform().inverse().get_matrix()[0, -1, :3].cpu().numpy()
        pl.add_mesh(frustum, style="wireframe", line_width=2)


def scene_pyt3d_to_gif(mesh_pyt3d, texture_img, G, gif_path, cameras=None):
    pl = pv.Plotter(shape=(1, 2), window_size=(2048, 1024), border=False, off_screen=True)
    mesh_pv, texture = mesh_pyt3d_to_pv(mesh_pyt3d)

    pl.subplot(0, 0)
    pl.set_viewup([0, 1, 0])
    pl.add_axes(line_width=5, labels_off=False)
    add_cameras(pl, cameras) if cameras is not None else None
    pl.add_mesh(mesh_pv, texture=texture_img[::-1], lighting=False)

    pl.subplot(0, 1)
    pl.set_viewup([0, 1, 0])
    add_cameras(pl, cameras) if cameras is not None else None
    pl.add_mesh(mesh_pv, texture=texture_img[::-1], lighting=False)

    line_sets = G_to_lineset_o3d(G)
    for line_set in line_sets:
        lines = np.array(line_set.lines).flatten()
        lines = np.append(lines[[0]], lines[1:][np.diff(lines) != 0])
        points = np.array(line_set.points)[lines]
        line = pv.lines_from_points(points)
        pl.add_mesh(line, lighting=False, copy_mesh=True, color=[1., 0., 0.], line_width=3,
                    render_lines_as_tubes=True)
        sleep(0.1)

    pl.link_views()
    path = pl.generate_orbital_path(n_points=36, shift=mesh_pv.length, viewup=[0, 1, 0])
    pl.open_gif(gif_path)
    pl.orbit_on_path(path, write_frames=True, viewup=[0, 1, 0])

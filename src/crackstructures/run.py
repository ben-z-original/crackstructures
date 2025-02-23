import warnings
from pathlib import Path
from enstrect.run import run
from argparse import ArgumentParser
from omnicrack30k.inference import OmniCrack30kModel
from crackstructures.mapping.fuser import NaiveMaxFuser

warnings.filterwarnings("ignore", message="Detected old nnU-Net plans")  # warning can be ignored


def run_crackstructures(obj_or_ply_path, cameras_path, images_dir, out_dir, select_views, num_points, scale):
    run(obj_or_ply_path, cameras_path, images_dir, out_dir, select_views, num_points, scale,
        model=OmniCrack30kModel, fuser=NaiveMaxFuser)


if __name__ == "__main__":
    parser = ArgumentParser(description="""Run enstrect for segmenting, mapping, and extracting structural cracks.""")
    parser.add_argument('-p', '--obj_or_ply_path', type=Path,
                        default=Path(__file__).parent / "assets" / "crackstructures" / "beam" /
                                "segment3" / "mesh" / "mesh.obj",
                        help="Path to the mesh (.obj; points will be sampled) or point cloud file (.ply).")
    parser.add_argument('-i', '--images_dir', type=Path,
                        default=Path(__file__).parent / "assets" / "crackstructures" / "beam" /
                                "segment3" / "views",
                        help="Path to the directory which contains the images/views.")
    parser.add_argument('-c', '--cameras_path', type=Path,
                        default=Path(__file__).parent / "assets" / "crackstructures" / "beam" /
                                "segment3" / "cameras.json",
                        help="Path to the file that contains the intrinsic and extrinsic camera information.")
    parser.add_argument('-o', '--out_dir', type=Path,
                        default=Path(__file__).parent / "assets" / "crackstructures" / "beam" /
                                "segment3" / "out",
                        help="Path to the directory where the results will be stored")
    parser.add_argument('-v', '--select_views', nargs='*', help="List of views that should be used.")
    parser.add_argument('-s', '--scale', type=float, default=0.25,
                        help="Rescale the images to be processed. Defaults is 0.25 to reduce runtime. " +
                             "Use 1.0 for full resolution.")
    parser.add_argument('-n', '--num_points', type=int, default=10 ** 6,
                        help="Number of points to sample from the mesh. Default is 1,000,000")
    args = parser.parse_args()

    run_crackstructures(args.obj_or_ply_path, args.cameras_path, args.images_dir,
                        args.out_dir, args.select_views, args.num_points, args.scale)

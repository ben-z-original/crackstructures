import argparse
from pathlib import Path
from enstrect.evaluation.run import evaluate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate and visualize results.")
    parser.add_argument('--datadir', type=Path,
                        default=Path(__file__).parents[1] / "assets" / "crackstructures",
                        help="Directory path to dataset root")
    parser.add_argument('--structure', type=str, default="beam", help="Structure type")
    parser.add_argument('--segment', type=str, default="segment3", help="Segment type")
    parser.add_argument('--damage', nargs='+', default="crack",
                        help="Structural damage (or list of structural damages, in case they form a combined class")
    parser.add_argument('--vis', action='store_true', help="Enable visualization")
    parser.add_argument('--result_dirname', type=str, default="out",
                        help="Name of the results directory for predicted damage files")
    parser.add_argument('--tex_path', type=Path, help="Path to save the tex output")
    args = parser.parse_args()

    segment_path = args.datadir / args.structure / args.segment

    evaluate(segment_path, args.damage, vis=args.vis, tex_path=args.tex_path, result_dirname=args.result_dirname)
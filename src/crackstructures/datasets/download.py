from pathlib import Path
from argparse import ArgumentParser
from enstrect.datasets.download import download

datasets = {
    "crackstructures": "https://drive.google.com/uc?id=1-zlLnlnHSvTrb69HQbATb7LrAAu4v5kc",
    "crackensembles": "https://drive.google.com/uc?id=13_-0uF0inOyw4iemlpop-O0iISid0o8e"
}

if __name__ == "__main__":
    parser = ArgumentParser(description="""Downloads the dataset to a given directoy path.""")
    parser.add_argument('dataset', nargs='?', type=str, default="crackstructures",
                        choices=datasets.keys(),
                        help="Name of the dataset to download.")
    parser.add_argument('-p', '--target_path', type=Path,
                        default=Path(__file__).parents[1] / "assets",
                        help="Directory where the dataset will be downloaded and unzipped.")
    args = parser.parse_args()

    download(args.dataset, datasets[args.dataset], args.target_path)

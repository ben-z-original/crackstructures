import gdown
import zipfile
import warnings
from pathlib import Path
from argparse import ArgumentParser


def download():
    parser = ArgumentParser(description="""Downloads the dataset to a given directoy path.""")
    parser.add_argument('-p', '--dir_path', type=Path,
                        default=Path(__file__).parent / "assets",
                        help="Directory where the dataset will be downloaded and unzipped.")
    args = parser.parse_args()

    # create directory (if needed)
    args.dir_path.mkdir(exist_ok=True)

    # doẃnload
    zippath = Path(args.dir_path / "crackstructures.zip")
    if not zippath.exists():
        url = "https://drive.google.com/uc?id=1-zlLnlnHSvTrb69HQbATb7LrAAu4v5kc"
        gdown.download(url, str(zippath), quiet=False)
    else:
        warnings.warn(f"The segments dataset already exists in the path: {zippath}", UserWarning)

    # unzip
    with zipfile.ZipFile(str(zippath), 'r') as zip_ref:
        zip_ref.extractall(str(args.dir_path / "crackstructures"))
        print("Successfully extraced")


if __name__ == "__main__":
    download()

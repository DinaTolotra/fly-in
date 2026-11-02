from pathlib import Path
import argparse


def main() -> None:
    argument_parser = argparse.ArgumentParser(
        prog="fly-in",
        description="A parallel and streamed path-finding simulation."
    )
    argument_parser.add_argument(
        "map_file",
        nargs="?",
        type=Path,
        default="maps/easy/01_linear_path.txt",
        help="map file to inspect (default: %(default)s)",
    )
    arguments = argument_parser.parse_args()
    print(arguments)

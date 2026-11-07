from pathlib import Path
import argparse


def get_arg() -> Path:
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
    argument = argument_parser.parse_args()
    return argument.map_file

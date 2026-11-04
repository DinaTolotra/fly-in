from pathlib import Path
import argparse

from .parser import Parser


def main() -> None:
    print("Welcome to Fly-in")
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
    parser = Parser(arguments.map_file)
    drone_count, hubs, connections = parser.parse()
    print(f"Drone count = {drone_count}")
    print(f"Hubs: {len(hubs)}")
    for hub in hubs:
        print(f"\t{hub.hub_name} {hub.hub_role} {hub.position}")
    print(f"Connection: {len(connections)}")
    for conn in connections:
        print(f"\t{conn.first.hub_name} {conn.second.hub_name} {conn.max_link_capacity}")

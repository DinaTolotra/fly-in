from pathlib import Path
import argparse

from .arg import get_arg
from .parser import Parser
from .gui import main as gui_main


def main() -> None:
    print("Welcome to Fly-in")
    map_file = get_arg()
    parser = Parser(map_file)
    drone_count, hubs, connections = parser.parse()
    gui_main(hubs)

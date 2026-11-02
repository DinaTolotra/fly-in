from pathlib import Path
from os import access, R_OK
import re

from . import model


class Parser():
    def __init__(self, file: Path) -> None:
        if not Parser._check_file_permission(file):
            raise ValueError(f"invalid path: {file.absolute()}")
        self.file = file
        
    def parse(self) -> tuple[int, model.Hub, model.Connection]:
        drone_number_pattern = re.compile(r"^nb_drones: (?P<nb>[0-9]+)$")
        hub_pattern = re.compile(r"^(?P<role>[a-zA-Z_]+): (?P<name>[a-zA-Z0-9_]+) (?P<x>[0-9]+) (?P<y>[0-9]+) (\[(?P<metadata>[- 0-9a-zA-Z=]+)\])?$")
        color_pattern = re.compile(r"(color=(?P<color>[a-zA-Z0-9]+))?")
        zone_pattern = re.compile(r"(zone=(?P<zone>[a-zA-Z0-9]+))?")
        max_drone_pattern = re.compile(r"(max_drones=(?P<max_drone>[a-zA-Z0-9]+))?")
        connection_pattern = re.compile(r"^connection: (?P<first>[a-zA-Z0-9_]+)-(?P<second>[a-zA-Z0-9_])$")

    @staticmethod
    def _check_file_permission(file: Path) -> bool:
        return file.is_file() and access(file, R_OK)

from pathlib import Path
from os import access, R_OK
import re

from pydantic.main import sys

from . import model


class ParseError(Exception):
    def __init__(
        self,
        file: str,
        line_nb: int,
        msg: str,
        *args: object
    ) -> None:
        message = f"failed to parse config file {file} lines {line_nb}: {msg}"
        super().__init__(message, *args)


class Parser():
    def __init__(self, path: Path) -> None:
        if not Parser._check_file_permission(path):
            raise ValueError(f"invalid path: {path.absolute()}")
        self.file = path
        self.data = Parser._read_file(path)
        self.drone_count_pattern = re.compile(
            r"^nb_drones: (?P<nb>[0-9]+)$"
        )
        self.hub_pattern = re.compile(
            r"^(?P<role>[a-zA-Z_]+):\s+(?P<name>[a-zA-Z0-9_]+)\s+"
            r"(?P<x>-?[0-9]+)\s+(?P<y>-?[0-9]+)"
            r"(?:\s+\[(?P<metadata>[^]]*)\])?$"
        )
        self.connection_pattern = re.compile(
            r"^connection:\s+(?P<first>[a-zA-Z0-9_]+)-"
            r"(?P<second>[a-zA-Z0-9_]+)"
            r"(?:\s+\[max_link_capacity=(?P<capacity>[0-9]+)\])?$"
        )

    def parse(
        self,
    ) -> tuple[int, list[model.Hub], list[model.Connection]]:
        drone_count: int | None = None
        hubs: dict[str, model.Hub] = {}
        connections: list[model.Connection] = []
        has_start_hub, has_end_hub = False, False

        for line_nb, raw_line in enumerate(self.data, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if len(line) == 0:
                continue

            if drone_count is None:
                drone_count = self.get_drone_count(line_nb)
                if drone_count is not None:
                    continue

            if line.startswith("connection:"):
                connections.append(self.get_connection(line_nb, hubs))
                continue

            hub = self.get_hub(line_nb)
            if hub.hub_name in hubs:
                raise ParseError(
                    self.file.absolute().name,
                    line_nb,
                    f"duplicate hub name: {hub.hub_name}"
                )
            if hub.hub_role is model.HubRole.START:
                if has_start_hub:
                    raise ParseError(
                        self.file.absolute().name, line_nb,
                        "duplicate start hub"
                    )
                else:
                    has_start_hub = True
            elif hub.hub_role is model.HubRole.END:
                if has_end_hub:
                    raise ParseError(
                        self.file.absolute().name, line_nb,
                        "duplicate start hub"
                    )
                else:
                    has_end_hub = True
            hubs[hub.hub_name] = hub

        if drone_count is None:
            raise ParseError(
                self.file.absolute().name,
                1,
                "missing drone count"
            )

        return drone_count, list(hubs.values()), connections

    def get_drone_count(self, line_nb: int) -> int:
        if line_nb > len(self.data):
            raise ValueError(f"invalid line number: {line_nb}")
        line = self.data[line_nb - 1]
        line = line.strip()
        drone_count = 0
        match = self.drone_count_pattern.fullmatch(line)
        if match is None:
            raise ParseError(
                self.file.absolute().name, line_nb,
                "first non-comment line must be drone count"
            )
        drone_count = int(match.group("nb"))
        if drone_count < 2:
            raise ParseError(
                self.file.absolute().name, line_nb,
                "drone count must be greater or equal than 2"
            )
        return drone_count

    def get_connection(
        self,
        line_nb: int,
        hubs: dict[str, model.Hub]
    ) -> model.Connection:
        if line_nb > len(self.data):
            raise ValueError(f"invalid line number: {line_nb}")
        line = self.data[line_nb - 1]
        line = line.strip()
        match = self.connection_pattern.fullmatch(line)
        if match is None:
            raise ParseError(
                self.file.absolute().name, line_nb,
                "invalid connection declaration"
            )
        first = hubs.get(match.group("first"))
        second = hubs.get(match.group("second"))
        if first is None or second is None:
            raise ParseError(
                self.file.absolute().name, line_nb,
                "unknown hub refered in connection"
            )
        connection = model.Connection(
            first=first,
            second=second,
            max_link_capacity=1,
        )
        capacity = match.group("capacity")
        if capacity is not None:
            link_capacity = int(capacity)
            if link_capacity < 1:
                raise ParseError(
                    self.file.absolute().name,
                    line_nb,
                    "max_link_capacity must be positive"
                )
            connection.max_link_capacity = link_capacity
        return connection

    def get_hub(self, line_nb: int) -> model.Hub:
        if line_nb > len(self.data):
            raise ValueError(f"invalid line number: {line_nb}")
        line = self.data[line_nb - 1]
        line = line.strip()
        match = self.hub_pattern.fullmatch(line)
        if match is None:
            raise ParseError(
                self.file.absolute().name,
                line_nb,
                "invalid hub declaration"
            )

        name = match.group("name")
        metadata: dict[str, str] = {}
        metadata_text = match.group("metadata")
        if metadata_text:
            for item in metadata_text.split():
                key, separator, value = item.partition("=")
                if not separator or not value or key in metadata:
                    raise ParseError(
                        self.file.absolute().name, line_nb,
                        f"invalid hub metadata format: {item}"
                    )
                if key not in {"zone", "color", "max_drones"}:
                    raise ParseError(
                        self.file.absolute().name, line_nb,
                        f"unknown hub metadata: {key}"
                    )
                metadata[key] = value

        try:
            role = model.HubRole(match.group("role"))
        except ValueError as error:
            raise ParseError(
                self.file.absolute().name,
                line_nb,
                f"invalid hub role: {match.group('role')}"
            ) from error

        hub_type = model.HubType.NORMAL
        if "zone" in metadata:
            try:
                hub_type = model.HubType(metadata["zone"])
            except ValueError as error:
                raise ParseError(
                    self.file.absolute().name,
                    line_nb,
                    f"invalid hub type: {metadata['zone']}"
                ) from error

        color = metadata.get("color")
        if (
            color is not None
            and re.fullmatch(r"[a-z]+", color) is None
        ):
            raise ParseError(
                self.file.absolute().name,
                line_nb,
                f"invalid hub color: {color}"
            )

        try:
            max_drones = int(metadata.get("max_drones", "1"))
        except ValueError as error:
            raise ParseError(
                self.file.absolute().name,
                line_nb,
                "max_drones must be a positive integer"
            ) from error
        if max_drones < 1:
            raise ParseError(
                self.file.absolute().name,
                line_nb,
                "max_drones must be positive"
            )

        hub = model.Hub(
            hub_role=role,
            hub_name=name,
            position=(int(match.group("x")), int(match.group("y"))),
            type=hub_type,
            color=color,
            max_drone=max_drones,
        )
        return hub

    @staticmethod
    def _read_file(file: Path) -> list[str]:
        data: list[str]
        with open(file, "r", encoding="utf-8") as f:
            try:
                data = f.readlines()
            except UnicodeDecodeError as error:
                raise RuntimeError("unexpected file encoding") from error
            except KeyboardInterrupt as error:
                raise RuntimeError("operation interupted by user") from error
            except OSError as error:
                raise RuntimeError("system-level I/O error occured") from error
        return data

    @staticmethod
    def _check_file_permission(file: Path) -> bool:
        return file.exists() and file.is_file() and access(file, R_OK)

from pathlib import Path
from os import access, R_OK

from . import model


class Parser():
    def __init__(self, file: Path) -> None:
        if not Parser._check_file_permission(file):
            raise ValueError(f"invalid path: {file.absolute()}")
        self.file = file
        
    def parse(self) -> tuple[int, model.Hub, model.Connection]:
        
        pass

    @staticmethod
    def _check_file_permission(file: Path) -> bool:
        return file.is_file() and access(file, R_OK)

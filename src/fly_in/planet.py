from pathlib import Path
from typing import Any
import pygame as pg


class Planet(pg.sprite.Sprite):
    def __init__(self, color: str, size: tuple[int, int]) -> None:
        super().__init__()
        path = Path(f"res\\planet.png")
        if not path.exists():
            raise RuntimeError(f"asset for planet with color {color} not found")
        self.sprite_sheet = Planet.load_spritesheet(path, size, 0.25)
        self.size = size
        self.image = self.sprite_sheet[0]
        self.rect = self.image.get_rect()
        self.frame_count = len(self.sprite_sheet)
        self.frame = 0
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.frame = self.frame + 1 if self.frame + 1 < self.frame_count else 0
        self.image = self.sprite_sheet[self.frame]
        return super().update(*args, **kwargs)
    
    @staticmethod
    def load_spritesheet(path: Path, frame: tuple[int, int], scale_factor: float = 1.) -> list[pg.Surface]:
        spritesheet: list[pg.Surface] = []
        image = pg.image.load(path).convert_alpha()
        fw, fh = frame
        w, h = image.get_size()
        fxc, fyc = w // fw, h // fh
        for y in range(fyc):
            for x in range(fxc):
                temp = image.subsurface(x * fw, y * fh, fw, fh)
                spritesheet.append(pg.transform.scale_by(temp, scale_factor))
        return spritesheet

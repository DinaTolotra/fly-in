import pygame as pg
import random

from .model import Hub
from .planet import Planet


def main(hubs: list[Hub]) -> None:
    pg.init()
    screen = pg.display.set_mode((800, 600))
    movable_surface = pg.surface.Surface((1500, 1000))
    pg.display.set_caption("Fly In GUI")
    clock = pg.time.Clock()
    planets = pg.sprite.Group()
    visible = pg.rect.Rect(0, 0, *screen.get_size())

    for hub in hubs:
        x, y = hub.position
        x, y = int(x) + 3, int(y) + 3
        if x < 100 and x < 100:
            planet = Planet(str(hub.color), (128, 128))
            planet.rect.topleft = (x * 32 * 2, y * 32 * 2)
            planets.add(planet)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    visible.left += 4
        planets.update()
        screen.fill((0, 0, 0))
        planets.draw(movable_surface)
        screen.blit(movable_surface.subsurface(visible), screen.get_rect())
        pg.display.flip()
        clock.tick(30)

    pg.quit()

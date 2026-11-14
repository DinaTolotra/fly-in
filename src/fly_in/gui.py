import pygame as pg

from .model import Hub


def main(hubs: list[Hub]) -> None:
    pg.init()
    win_size = (800, 600)
    screen = pg.display.set_mode(win_size)
    pg.display.set_caption("Fly In GUI")
    clock = pg.time.Clock()
    hub_size = (10, 10)
    hub_layer = pg.Surface((1000, 1000)).convert_alpha()
    hub_view = pg.Surface(hub_size).convert_alpha()
    pg.draw.rect(hub_view, pg.Color(255, 255, 255, 255), (0, 0, 10, 10))

    for hub in hubs:
        hub_layer.blit(
            hub_view,
            (
                hub.position[0] * hub_size[0],
                hub.position[1] * hub_size[1]
            )
        )

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.blit(hub_layer, (0, 0))
        pg.display.flip()
        clock.tick(60)

    pg.quit()

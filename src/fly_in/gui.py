import pygame as pg


def main() -> None:
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Fly In GUI")
    clock = pg.time.Clock()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill((0, 0, 0))
        pg.display.update()
        clock.tick(60)

    pg.quit()

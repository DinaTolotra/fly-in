import sys
import pygame as pg


def init_gui() -> pg.Surface:
    pg.init()
    canva = pg.display.set_mode((800, 640), pg.RESIZABLE)    
    pg.display.set_caption("Fly-in")
    canva.fill(pg.Color(255, 255, 255))
    pg.display.update()
    return canva


def main() -> None:
    print("Hello world, welcome to Fly-in!")
    print("[LOG] Initializing pygame", file=sys.stderr)
    init_gui()

    loop = True

    print("[LOG] Starting event loop", file=sys.stderr)
    while loop:
        event_list = pg.event.get()
        processed = 0
        ignored = 0
        failed = 0
        print(f"[LOG] Caught [{len(event_list)}] event(s)", file=sys.stderr)
        for i, event in enumerate(event_list):
            try:
                if event.type == pg.QUIT:
                    print(f"[LOG] Received [quit] signal", file=sys.stderr)
                    processed += 1
                    loop = False
                else:
                    print(f"[LOG] Ignoring event [{i}]:", pg.event.event_name(event.type), file=sys.stderr)
                    ignored += 1
            except Exception as error:
                print("[ERR] Failed to process event:", pg.event.event_name(event.type), file=sys.stderr)
                failed += 1
        if len(event_list) != 0:
            print("[LOG] Event processing feedback:", file=sys.stderr)
            print("[LOG] ... processed =", processed, file=sys.stderr)
            print("[LOG] ... ignored =", ignored, file=sys.stderr)
            print("[LOG] ... failed =", failed, file=sys.stderr)
            print("[LOG]", file=sys.stderr)
            
    pg.quit()

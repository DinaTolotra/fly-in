from functools import reduce

from fly_in.model import Hub


def normalize_hub(hubs: list[Hub]) -> None:
    min_x = reduce(lambda h1, h2: h1 if h1.position[0] < h2.position[0] else h2, hubs)
    min_y = reduce(lambda h1, h2: h1 if h1.position[1] < h2.position[1] else h2, hubs)
    for hub in hubs:
        hub.position = (
            hub.position[0] + abs(min_x.position[0]),
            hub.position[1] + abs(min_y.position[1]),
        )